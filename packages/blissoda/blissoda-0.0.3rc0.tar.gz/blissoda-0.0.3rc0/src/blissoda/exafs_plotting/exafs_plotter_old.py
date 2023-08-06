"""Workflow execution and Flint EXAFS plotting during a scan"""

import time
import os
import gevent
from collections import OrderedDict
from typing import List, Optional, Tuple

from silx.io.h5py_utils import top_level_names

try:
    from bliss.common.plot import get_flint
    from bliss.flint.client.plots import BasePlot
    from bliss.flint.client.proxy import FlintClient
except ImportError:
    get_flint = None
    BasePlot = None
    FlintClient = None

from ewoksjob.client import submit
from ewoksjob.client import get_future
from ..utils.info import format_info


class ExafsPlotter:
    """Run a scan, execute a workflow every x seconds during the scan
    and plot the results in Flint. A fixed number of n scans stay plotted.
    """

    def __init__(self) -> None:
        self._scans = OrderedDict()  # scan_id -> scan_info
        self._plots = dict()  # plot_id -> plot_info
        self._client = None
        self._color_index = 0
        self._scan_type = None

        # Parameters (could be in beacon):
        self.workflow = None
        self._plot_names = {
            "flatten_mu": "mu(E)",
            "chi_weighted_k": "chi(k)",
            "ft_mag": "FT",
            "noise_savgol": "Noise",
        }  # plot_id -> plot_name
        self._counters = dict()
        self.refresh_period = 2  # seconds
        self.max_scans = 3
        self.enabled = True

    @property
    def counters(self):
        return self._counters[self.scan_type]

    @property
    def scan_type(self):
        return self._scan_type

    @scan_type.setter
    def scan_type(self, value):
        assert value in self._counters
        self._scan_type = value

    @property
    def mu_name(self):
        return self.counters["mu_name"]

    @mu_name.setter
    def mu_name(self, value):
        self.counters["mu_name"] = value

    @property
    def energy_name(self):
        return self.counters["energy_name"]

    @energy_name.setter
    def energy_name(self, value):
        self.counters["energy_name"] = value

    @property
    def energy_unit(self):
        return self.counters["energy_unit"]

    @energy_unit.setter
    def energy_unit(self, value):
        self.counters["energy_unit"] = value

    def _scan_type_from_scan(self, scan) -> str:
        raise NotImplementedError

    def run(self, scan):
        if not self.enabled:
            scan.run()
            return

        self.scan_type = self._scan_type_from_scan(scan)

        filename = scan.writer.filename
        if os.path.exists(filename):
            scannr = max(int(float(s)) for s in top_level_names(filename)) + 1
        else:
            scannr = 1
        scan_legend = f"{scannr}.1"
        scan_url = f"silx://{filename}::/{scannr}.1"
        scan_id = scan_url
        scan_name = os.path.split(os.path.dirname(filename))[-1]
        scan_name = f"{scan_name}:{scannr}.1"
        scan_color = self._COLOR_PALETTE[self._color_index]
        self._color_index = (self._color_index + 1) % len(self._COLOR_PALETTE)
        args = scan_id, scan_name, scan_legend, scan_color, scan_url

        update_loop = gevent.spawn(self._plotting_loop, *args)
        try:
            scan.run()
        finally:
            try:
                if not update_loop:
                    update_loop.get()
                update_loop.kill()
                self._submit_and_plot(scan_id)
            finally:
                self._removed_failed_processing()
                self._purge_plots()

    def clear(self):
        """Remove all scan curves in all plots"""
        for plot_id in self._plot_names:
            self._get_plot(plot_id).clear_items()

    def refresh(self):
        """Refresh all plots with the current processed data"""
        for scan_id in self._scans:
            self._update_scan_plot(scan_id)

    def reprocess(self):
        """Reprocess all scans and update all curves"""
        for scan_id in self._scans:
            self._submit_and_plot(scan_id)

    def dump(self) -> List[Tuple[str, dict]]:
        essential = "job_id", "scan_url", "scan_legend"
        return [
            (scan_id, {k: v for k, v in info.items() if k in essential})
            for scan_id, info in self._scans.items()
        ]

    def load(self, data: List[Tuple[str, dict]]) -> None:
        for scan_id, scan_info in data:
            self._init_scan_cache(scan_id, **scan_info)
        self.refresh()

    def _submit_and_plot(self, scan_id: str):
        self._submit_workfow(scan_id)
        self._update_scan_plot(scan_id)

    def _plotting_loop(
        self,
        scan_id: str,
        scan_name: str,
        scan_legend: str,
        scan_color: tuple,
        scan_url: str,
    ):
        self._init_scan_cache(
            scan_id,
            scan_name=scan_name,
            scan_legend=scan_legend,
            scan_color=scan_color,
            scan_url=scan_url,
        )
        t0 = time.time()
        while True:
            t1 = time.time()
            sleep_time = max(t0 + self.refresh_period - t1, 0)
            gevent.sleep(sleep_time)
            t0 = t1
            self._submit_and_plot(scan_id)

    def _init_scan_cache(self, scan_id: str, **kw):
        scan_info = self._scans.get(scan_id)
        if scan_info is not None:
            return
        scan_info = {
            "job_id": None,
            "future": None,
            "result": None,
            "previous_result": None,
            "scan_legend": None,
            "scan_url": None,
            "scan_name": None,
            "scan_color": None,
        }
        scan_info.update(kw)
        self._scans[scan_id] = scan_info
        return scan_info

    def _purge_plots(self, max_scans=None):
        if max_scans is None:
            max_scans = self.max_scans
        npop = max(len(self._scans) - max_scans, 0)
        for _ in range(npop):
            _, scan_info = self._scans.popitem(last=False)
            self._remove_scan_plot(scan_info["scan_legend"])

    def remove_scan(self, scan_legend: str):
        scans = OrderedDict()
        for scan_id, scan_info in self._scans.items():
            if scan_info["scan_legend"] == scan_legend:
                self._remove_scan_plot(scan_legend)
            else:
                scans[scan_id] = scan_info
        self._scans = scans

    def _removed_failed_processing(self):
        scans = OrderedDict()
        for scan_id, scan_info in self._scans.items():
            if scan_info["previous_result"]:
                scans[scan_id] = scan_info
            else:
                self._remove_scan_plot(scan_info["scan_legend"])
        self._scans = scans

    def _remove_scan_plot(self, legend: str):
        for plot in self._plots.values():
            try:
                plot.remove_item(legend=legend)
            except Exception:
                pass  # plot may not exist anymore
            try:
                plot.added_curves.remove(legend)
            except KeyError:
                pass  # plot was created

    def _update_scan_plot(self, scan_id: str):
        """Update all scan curves in all plots"""
        client = self._get_client()
        for plot_id in self._plot_names:
            plot = self._plots.get(plot_id)
            if plot is None or not client.is_plot_exists(plot_id):
                # Create a fresh plot with all scan curves
                for _scan_id in self._scans:
                    self._update_scan_curve(plot_id, _scan_id, plot=plot)
            else:
                # Update the existing plot for the requested scan
                self._update_scan_curve(plot_id, scan_id)

    def _update_scan_curve(self, plot_id: str, scan_id: str, plot=None):
        """Update the scan curve in a specific plot"""
        result, scan_info = self._get_data(scan_id)
        if result is None:
            return
        result = result[plot_id]
        plot = self._get_plot(plot_id)
        plot.xlabel = result["xlabel"]
        plot.ylabel = result["ylabel"]

        # plot.add_curve(result["x"], result["y"], legend=legend)
        # return

        legend = scan_info["scan_legend"]
        suffix = legend.replace(".", "_")
        xname = "x" + suffix
        yname = "y" + suffix
        kw = {xname: result["x"], yname: result["y"]}

        try:
            if legend not in plot.added_curves:
                plot.add_curve_item(
                    xname, yname, legend=legend, color=scan_info["scan_color"]
                )
                plot.added_curves.add(legend)

            plot.set_data(**kw)
        except AttributeError:
            pass  # someone closed the plot

    def _get_plot(self, plot_id: str) -> BasePlot:
        """Launches Flint and creates the plot when either is missing"""
        client = self._get_client()
        plot = self._plots.get(plot_id)
        if plot is None or not client.is_plot_exists(self._plot_names[plot_id]):
            plot = client.get_plot("curve", unique_name=self._plot_names[plot_id])
            self._plots[plot_id] = plot
            plot.added_curves = set()
        return plot

    def _get_client(self) -> FlintClient:
        """Launches Flint when missing"""
        if self._client is None or not self._client.is_available():
            self._client = get_flint()
        return self._client

    def _get_data(self, scan_id: str) -> Optional[Tuple[dict, dict]]:
        """Get data and curve legend for a scan when available.
        Blocks when the workflow for the scan is still running"""
        scan_info = self._scans.get(scan_id)
        if scan_info is None:
            return scan_info["previous_result"], scan_info
        result = scan_info.get("result")
        if result is not None:
            return result, scan_info
        future = scan_info.get("future")
        if future is None:
            job_id = scan_info.get("job_id")
            if job_id is None:
                return scan_info["previous_result"], scan_info
            future = scan_info["future"] = get_future(job_id)
        try:
            result = future.get()
        except Exception:
            return scan_info["previous_result"], scan_info
        result = result["plot_data"]
        scan_info["previous_result"] = result
        scan_info["result"] = result
        return result, scan_info

    def _submit_workfow(self, scan_id: str) -> None:
        """Submit the data processing for a scan"""
        scan_info = self._scans.get(scan_id)
        if not scan_info or not scan_info["scan_url"]:
            return
        inputs = list()
        input_information = {
            "channel_url": f"{scan_info['scan_url']}/measurement/{self.energy_name}",
            "spectra_url": f"{scan_info['scan_url']}/measurement/{self.mu_name}",
            "energy_unit": self.energy_unit,
        }
        inputs.append(
            {
                "label": "xas input",
                "name": "input_information",
                "value": input_information,
            }
        )
        inputs.append(
            {
                "label": "plotdata",
                "name": "plot_names",
                "value": list(self._plot_names),
            }
        )
        future = submit(args=(self.workflow,), kwargs={"inputs": inputs})
        scan_info["future"] = future
        scan_info["job_id"] = future.task_id
        scan_info["result"] = None

    def __info__(self) -> str:
        return f"Parameters:\n {self._param_info()}\n\nProcessing:\n {self._process_info()}\n\nPlots:\n {self._plot_info()}"

    def _process_info(self) -> str:
        return "\n ".join(
            [
                f"Scan {scan_info['scan_name']}, Job {scan_info['job_id']}, Processed = {bool(scan_info['previous_result'])}"
                for scan_info in self._scans.values()
            ]
        )

    def _plot_info(self) -> str:
        return "\n ".join(
            [f"{plot_id}: {plot}" for plot_id, plot in self._plots.items()]
        )

    def _param_info(self) -> str:
        info = {
            "enabled": self.enabled,
            "scan_type": self.scan_type,
            "workflow": self.workflow,
            "mu": self.mu_name,
            "energy": self.energy_name,
            "energy_unit": self.energy_unit,
            "refresh_period": self.refresh_period,
            "max_scans": self.max_scans,
        }
        return format_info(info)

    _COLOR_PALETTE = [
        (87, 81, 212),
        (235, 171, 33),
        (176, 69, 0),
        (0, 197, 248),
        (207, 97, 230),
        (0, 166, 107),
        (184, 0, 87),
        (0, 138, 248),
        (0, 110, 0),
        (0, 186, 171),
        (255, 145, 133),
        (133, 133, 0),
    ]
