import os
import json
import logging
import tempfile
from glob import glob
from typing import Optional, List, MutableMapping

try:
    from bliss.scanning import scan_meta
    from bliss import current_session
except ImportError:
    scan_meta = None
    current_session = None

from ewoksjob.client import submit, convert_workflow

from ..persistent import WithPersistentParameters
from ..resources.id11 import RESOURCE_ROOT
from ..utils.directories import get_processed_dir, get_collection_dir
from ..utils.pyfai import read_config
from ..utils.info import format_info

logger = logging.getLogger(__name__)


_WORKERS = "lid11eiger2lima", "lid11detector"


class XrpdProcessor(
    WithPersistentParameters,
    parameters=[
        "enabled",
        "workflow",
        "detector_name",
        "counter_names",
        "pyfai_config_directory",
        "_integration_options",
        "retry_timeout",
        "monitor_name",
        "reference",
        "worker",
    ],
):
    def __init__(self) -> None:
        super().__init__()
        if current_session is None:
            raise ImportError("blissdata")
        self._set_parameter_default("enabled", False)
        self._set_parameter_default("_integration_options", dict())
        self._set_parameter_default("pyfai_config_directory", tempfile.gettempdir())
        default_workflow = os.path.join(RESOURCE_ROOT, "integrate_scan.ows")
        self._set_parameter_default("workflow", default_workflow)
        self._sync_scan_metadata()

    def _modify_info(self, info: dict) -> None:
        if self.detector_name:
            info["integration_options"] = self._format_info("... (see below)")

    def __info__(self):
        s = super().__info__()
        if not self.detector_name:
            return s
        info = {
            "1. JSON file": self._detector_config_filename(".json"),
            "2. PONI file": self._detector_config_filename(".poni"),
            "3. User": self._format_info(self.integration_options),
            "Merged": self._format_info(self._merged_integration_options),
        }
        return f"{s}\n\nPyFai integration:\n " + format_info(info)

    @property
    def integration_options(self) -> Optional[MutableMapping]:
        detector_name = self.detector_name
        if not detector_name:
            return
        return self._integration_options.setdefault(detector_name, dict())

    @property
    def _merged_integration_options(self) -> dict:
        """Options from user, latest pyfai json file and latest pyfai poni file.
        The user parameters take priority over the poni parameters which take priority over the json parameters.
        """
        options = self._default_azint_options()
        options.update(self._default_calib_options())
        if self.detector_name:
            integration_options = self.integration_options
            if integration_options:
                options.update(integration_options.to_dict())
        return options

    def enable(self, detector) -> None:
        self.enabled = True
        self.detector_name = detector.name
        self._sync_scan_metadata()

    def disable(self) -> None:
        self.enabled = False
        self.detector_name = None
        self._sync_scan_metadata()

    def _detector_config_filename(self, ext: str) -> Optional[str]:
        detector_name = self.detector_name
        if not detector_name:
            return
        pyfai_config_directory = self.pyfai_config_directory
        if not pyfai_config_directory:
            pyfai_config_directory = tempfile.gettempdir()
        pattern = os.path.join(pyfai_config_directory, detector_name, f"*{ext}")
        files = sorted(glob(pattern))
        if not files:
            return
        return files[-1]

    def _default_azint_options(self) -> dict:
        filename = self._detector_config_filename(".json")
        return read_config(filename)

    def _default_calib_options(self) -> dict:
        filename = self._detector_config_filename(".poni")
        return read_config(filename)

    def _sync_scan_metadata(self):
        scan_meta_obj = scan_meta.get_user_scan_meta()
        if self.enabled:
            if "workflows" not in scan_meta_obj.used_categories_names():
                scan_meta_obj.add_categories({"workflows"})
            scan_meta_obj.workflows.timing = scan_meta.META_TIMING.START
            scan_meta_obj.workflows.set("@NX_class", {"@NX_class": "NXcollection"})
            scan_meta_obj.workflows.set("nxprocess1", self._get_nxprocess1_content)
        else:
            scan_meta_obj.remove_categories({"workflows"})

    def _get_nxprocess1_content(self, scan) -> Optional[dict]:
        if not scan.scan_info.get("save"):
            return
        filename = scan.scan_info.get("filename")
        if not filename:
            return
        scan_nb = scan.scan_info.get("scan_nb")
        if not scan_nb:
            return
        detector_name = self.detector_name
        if not detector_name:
            return
        detector_info = scan.scan_info.get("channels", dict()).get(
            f"{detector_name}:image"
        )
        if not detector_info:
            return None

        nxprocess_name = os.path.splitext(os.path.basename(self.workflow))[0]
        future = convert_workflow(args=(self.workflow, None), queue=self._queue)
        workflow = future.get(timeout=10)
        inputs = self._get_inputs(scan, workflow)
        nxprocess1 = {
            nxprocess_name: {
                "@NX_class": "NXprocess",
                "program": "ewoks",
                "workflow": json.dumps(workflow),
                "inputs": json.dumps(inputs),
            }
        }

        convert_destination = self._save_workflow_filename(filename, scan_nb)
        submit(
            args=(self.workflow,),
            kwargs={
                "convert_destination": convert_destination,
                "save_options": {"indent": 2},
                "inputs": inputs,
            },
            queue=self._queue,
        )
        return nxprocess1

    @property
    def _queue(self):
        if self.worker not in _WORKERS:
            return None
        return self.worker

    def _integrate_node(self, workflow: dict) -> str:
        for nodeattrs in workflow["nodes"]:
            if ".integrate." in nodeattrs["task_identifier"]:
                return nodeattrs["task_identifier"]
        return "IntegrateBlissScan"

    def _save_nexus_node(self, workflow: dict) -> str:
        for nodeattrs in workflow["nodes"]:
            if ".nexus." in nodeattrs["task_identifier"]:
                return nodeattrs["task_identifier"]
        return "SaveNexusIntegrated"

    def _save_nexus_url(self, filename: str, scan_nb: str) -> str:
        root = get_processed_dir(filename)
        subdir = os.path.basename(get_collection_dir(filename))
        basename = os.path.basename(filename)
        filename = os.path.join(root, subdir, basename)
        return f"silx://{filename}::{scan_nb}.1"

    def _save_workflow_filename(self, filename: str, scan_nb: str) -> str:
        root = get_processed_dir(filename)
        subdir = os.path.basename(get_collection_dir(filename))
        basename = os.path.splitext(os.path.basename(filename))[0]
        basename = f"{basename}_{scan_nb}.json"
        return os.path.join(root, subdir, "workflows", basename)

    def _get_inputs(self, scan, workflow: dict) -> List[dict]:
        detector_name = self.detector_name
        filename = scan.scan_info.get("filename")
        scan_nb = scan.scan_info.get("scan_nb")
        counter_names = self.counter_names
        retry_timeout = self.retry_timeout
        monitor_name = self.monitor_name
        reference = self.reference
        integration_options = self._merged_integration_options
        integrate_identifier = self._integrate_node(workflow)
        inputs = [
            {
                "task_identifier": integrate_identifier,
                "name": "filename",
                "value": filename,
            },
            {
                "task_identifier": integrate_identifier,
                "name": "scan",
                "value": scan_nb,
            },
            {
                "task_identifier": integrate_identifier,
                "name": "detector_name",
                "value": detector_name,
            },
            {
                "task_identifier": integrate_identifier,
                "name": "monitor_name",
                "value": monitor_name,
            },
            {
                "task_identifier": integrate_identifier,
                "name": "reference",
                "value": reference,
            },
            {
                "task_identifier": integrate_identifier,
                "name": "maximum_persistent_workers",
                "value": 1,
            },
        ]
        if counter_names:
            inputs.append(
                {
                    "task_identifier": integrate_identifier,
                    "name": "counter_names",
                    "value": counter_names,
                }
            )
        if retry_timeout:
            inputs.append(
                {
                    "task_identifier": integrate_identifier,
                    "name": "retry_timeout",
                    "value": retry_timeout,
                }
            )
        if integration_options:
            inputs.append(
                {
                    "task_identifier": "PyFaiConfig",
                    "name": "integration_options",
                    "value": integration_options,
                }
            )
        inputs.append(
            {
                "task_identifier": self._save_nexus_node(workflow),
                "name": "url",
                "value": self._save_nexus_url(filename, scan_nb),
            }
        )
        return inputs
