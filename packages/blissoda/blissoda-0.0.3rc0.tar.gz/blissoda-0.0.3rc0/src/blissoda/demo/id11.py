import os
import json
import numpy
from typing import List
from ..id11.xrpd_processor import XrpdProcessor

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None


def energy_wavelength(x):
    """keV to m and vice versa"""
    return 12.398419843320026 * 1e-10 / x


class DemoXrpdProcessor(XrpdProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._ensure_pyfai_config()

    def _ensure_pyfai_config(self):
        os.makedirs(
            os.path.join(self.pyfai_config_directory, "difflab6"), exist_ok=True
        )
        cfgfile = os.path.join(self.pyfai_config_directory, "difflab6", "latest.json")
        data = {
            "method": "no_csr_cython",
            "nbpt_rad": 4096,
            "unit": "q_nm^-1",
        }
        with open(cfgfile, "w") as f:
            json.dump(data, f)

        cfgfile = os.path.join(self.pyfai_config_directory, "difflab6", "latest.poni")
        with open(cfgfile, "w") as f:
            f.write("poni_version: 2\n")
            f.write("Detector: Pilatus1M\n")
            f.write("Detector_config: {}\n")
            f.write("Distance: 5e-2\n")
            f.write("Poni1: 10e-2\n")
            f.write("Poni2: 10e-2\n")
            f.write(f"Rot1: {numpy.radians(10)}\n")
            f.write("Rot2: 0\n")
            f.write("Rot3: 0\n")
            f.write(f"Wavelength: {energy_wavelength(12)}\n")

    def _get_inputs(self, scan, workflow: dict) -> List[dict]:
        lst = super()._get_inputs(scan, workflow)
        integrate_identifier = self._integrate_node(workflow)
        lst.append(
            {
                "task_identifier": integrate_identifier,
                "name": "demo",
                "value": True,
            },
        )
        return lst

    def test(self, npoints=10, expo=0.1):
        setup_globals.loopscan(
            npoints,
            expo,
            setup_globals.difflab6,
            setup_globals.diode1,
            setup_globals.diode2,
        )


if setup_globals is None:
    xrpd_processor = None
else:
    xrpd_processor = DemoXrpdProcessor()
