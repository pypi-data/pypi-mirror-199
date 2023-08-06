import numpy
import json

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None
from ..id31.xrpd_processor import XrpdProcessor


def energy_wavelength(x):
    """keV to m and vice versa"""
    return 12.398419843320026 * 1e-10 / x


_DEFAULT_CALIB = {
    "dist": 5e-2,  # 5 cm
    "poni1": 10e-2,  # 10 cm
    "poni2": 10e-2,  # 10 cm
    "rot1": numpy.radians(10),  # 10 deg
    "rot2": 0,  # 0 deg
    "rot3": 0,  # 0 deg
    "wavelength": energy_wavelength(12),  # 12 keV
    "detector": "Pilatus1M",
}


class DemoXrpdProcessor(XrpdProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._set_parameter_default(
            "integration_options",
            {
                "method": "no_csr_cython",
                "nbpt_rad": 1024,
                "radial_range_min": 1,
                "unit": "q_nm^-1",
            },
        )
        self._ensure_pyfai_config()

    def get_inputs(self, scan):
        self._ensure_pyfai_config()
        lst = super().get_inputs(scan)
        lst.append({"id": "integrate", "name": "demo", "value": True})
        return lst

    def _ensure_pyfai_config(self):
        if self.pyfai_config:
            return
        cfgfile = "/tmp/test.json"
        poni = _DEFAULT_CALIB
        with open(cfgfile, "w") as f:
            json.dump(poni, f)
        self.pyfai_config = cfgfile

    def enable(self):
        super().enable("difflab6", counter_names=["diode1", "diode2"])

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
    try:
        xrpd_processor = DemoXrpdProcessor()
    except ImportError:
        xrpd_processor = None
