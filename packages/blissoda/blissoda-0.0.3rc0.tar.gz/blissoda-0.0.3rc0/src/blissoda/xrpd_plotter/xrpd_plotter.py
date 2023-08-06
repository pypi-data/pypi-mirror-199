from time import time
from ..persistent import WithPersistentParameters

try:
    import gevent
    from bliss import current_session
    from bliss.common.logtools import log_exception
    from blissdata.data.node import get_session_node
except ImportError:
    gevent = None
    current_session = None
    scan_meta = None
    get_node = None

try:
    from bliss.common.plot import get_flint
    from bliss.flint.client.plots import BasePlot
    from bliss.flint.client.proxy import FlintClient
except ImportError:
    get_flint = None
    BasePlot = None
    FlintClient = None

from ewoksjob.client import submit

from ..utils.info import format_info


class XrpdPlotter(
    WithPersistentParameters,
    parameters=[
        "enabled",
        "pyfai_configurations",
        "integration_options",
        "trigger_period",
        "wait_for_results",
        "plot_name",
    ],
):
    def __init__(self) -> None:
        super().__init__()
        self._set_parameter_default("enabled", False)
        self._set_parameter_default("pyfai_configurations", dict())
        self._set_parameter_default("trigger_period", 1)
        self._set_parameter_default("wait_for_results", 10)
        self._set_parameter_default("plot_name", "pyfai")

        self._background_task = None
        self._workflow_tasks = dict()
        self._start_times = dict()

        self._plot = None
        self._client = None

        self._ensure_background_task()

    def _modify_info(self, info: dict) -> None:
        info.pop("enabled", None)

    def __info__(self):
        s = super().__info__()
        info = {
            "Active": bool(self._background_task),
            "Running workflows": len(self._workflow_tasks),
        }
        return f"{s}\n\nStatus:\n " + format_info(info)

    def enable(self):
        self.enabled = True
        self._ensure_background_task()

    def disable(self):
        self.enabled = False
        self._ensure_background_task()

    def _ensure_background_task(self):
        if self.enabled:
            if self._background_task:
                return
            self._kill_workflow_tasks()
            self._background_task = gevent.spawn(self._background_main)
        else:
            if not self._background_task:
                return
            self._background_task.kill()
            self._background_task.join()
            self._kill_workflow_tasks()

    def _kill_workflow_tasks(self):
        tasks = list(self._workflow_tasks.values())
        gevent.killall(tasks)
        gevent.joinall(tasks)
        self._workflow_tasks = dict()

    def _background_main(self):
        node = get_session_node(current_session.name)
        detectors = dict()
        for ev in node.walk_on_new_events(include_filter=("lima", "scan")):
            try:
                if ev.node.type == "lima":
                    lima_name = ev.node.parent.name
                    pyfai_config = self.pyfai_configurations.get(lima_name)
                    if not pyfai_config:
                        continue
                    for scan_db_name, nodes in detectors.items():
                        if ev.node.db_name.startswith(scan_db_name):
                            nodes[lima_name] = ev.node
                            self._trigger_workflow(lima_name, pyfai_config, ev.node)
                            break
                elif ev.node.type == "scan":
                    if ev.type == ev.type.NEW_NODE:
                        detectors[ev.node.db_name] = dict()
                    elif ev.type == ev.type.END_SCAN:
                        nodes = detectors.pop(ev.node.db_name, dict())
                        for lima_name, node in nodes.items():
                            pyfai_config = self.pyfai_configurations.get(lima_name)
                            if not pyfai_config:
                                continue
                            self._trigger_workflow(
                                lima_name, pyfai_config, node, force=True
                            )
            except Exception:
                log_exception(self, "error in XRPD plotter background task")
                raise

    def _trigger_workflow(
        self, lima_name: str, pyfai_config: str, node, force: bool = False
    ):
        """Trigger workflow and plot results in Flint"""
        db_name = node.db_name
        key = pyfai_config, db_name
        start_time = time()
        task = self._workflow_tasks.get(key)
        if task:
            return  # workflow is still running
        elif not force:
            previous_start_time = self._start_times.get(key, 0)
            if (start_time - previous_start_time) < self.trigger_period:
                return  # too soon after the last workflow
        task = gevent.spawn(self._trigger_main, lima_name, pyfai_config, db_name)
        self._start_times[key] = start_time
        self._workflow_tasks[key] = task

    def _trigger_main(self, lima_name: str, pyfai_config: str, db_name: str):
        """Trigger workflow and plot results in Flint"""
        try:
            inputs = self._get_inputs(pyfai_config, db_name)
            workflow = self._get_workflow()
            future = submit(args=(workflow,), kwargs={"inputs": inputs})
            try:
                result = future.get(timeout=self.wait_for_results)
            except Exception:
                return
            self._update_plot(lima_name, result)
        finally:
            key = pyfai_config, db_name
            self._workflow_tasks.pop(key, None)

    def _update_plot(self, lima_name: str, result: dict):
        plot = self._get_plot()
        plot.xlabel = result["xunits"]
        xname = f"x{lima_name}"
        yname = f"y{lima_name}"
        plot.add_curve_item(xname, yname, legend=lima_name)
        data = {xname: result["x"], yname: result["y"]}
        plot.set_data(**data)

    def _get_inputs(self, pyfai_config, db_name):
        lst = [
            {"id": "config", "name": "filename", "value": pyfai_config},
            {"id": "load_image", "name": "db_name", "value": db_name},
            {
                "id": "integrate",
                "name": "maximum_persistent_workers",
                "value": len(self.pyfai_configurations),
            },
        ]
        integration_options = self.integration_options
        if integration_options:
            lst.append(
                {
                    "id": "config",
                    "name": "integration_options",
                    "value": integration_options.to_dict(),
                }
            )
        return lst

    def _get_workflow(self):
        return {
            "graph": {"id": "pyfai_workflow"},
            "nodes": [
                {
                    "id": "config",
                    "task_type": "class",
                    "task_identifier": "ewoksxrpd.tasks.pyfaiconfig.PyFaiConfig",
                },
                {
                    "id": "load_image",
                    "task_type": "class",
                    "task_identifier": "ewoksxrpd.tasks.bliss.LastLimaImage",
                },
                {
                    "id": "integrate",
                    "task_type": "class",
                    "task_identifier": "ewoksxrpd.tasks.integrate.Integrate1D",
                },
            ],
            "links": [
                {
                    "source": "config",
                    "target": "integrate",
                    "data_mapping": [
                        {"source_output": "energy", "target_input": "energy"},
                        {"source_output": "detector", "target_input": "detector"},
                        {
                            "source_output": "detector_config",
                            "target_input": "detector_config",
                        },
                        {"source_output": "geometry", "target_input": "geometry"},
                        {"source_output": "mask", "target_input": "mask"},
                        {
                            "source_output": "integration_options",
                            "target_input": "integration_options",
                        },
                    ],
                },
                {
                    "source": "load_image",
                    "target": "integrate",
                    "data_mapping": [
                        {"source_output": "image", "target_input": "image"},
                    ],
                },
            ],
        }

    def _get_plot(self) -> BasePlot:
        """Launches Flint and creates the plot when either is missing"""
        client = self._get_client()
        if self._plot is None or not client.is_plot_exists(self.plot_name):
            self._plot = client.get_plot("curve", unique_name=self.plot_name)
        return self._plot

    def _get_client(self) -> FlintClient:
        """Launches Flint when missing"""
        if self._client is None or not self._client.is_available():
            self._client = get_flint()
        return self._client
