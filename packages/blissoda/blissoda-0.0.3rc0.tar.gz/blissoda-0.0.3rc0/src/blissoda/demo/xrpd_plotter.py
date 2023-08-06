import numpy
import json

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None
from ..xrpd_plotter.xrpd_plotter import XrpdPlotter


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


class DemoXrpdPlotter(XrpdPlotter):
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

    def _get_inputs(self, pyfai_config, db_name):
        self._ensure_pyfai_config()
        lst = super()._get_inputs(pyfai_config, db_name)
        lst += [{"id": "load_image", "name": "demo", "value": True}]
        return lst

    def _ensure_pyfai_config(self):
        cfgfile = "/tmp/test.json"
        self.pyfai_configurations["difflab6"] = cfgfile
        poni = _DEFAULT_CALIB
        with open(cfgfile, "w") as f:
            json.dump(poni, f)

    def test(self, npoints=100, expo=0.1):
        setup_globals.loopscan(
            npoints,
            expo,
            setup_globals.difflab6,
            setup_globals.diode1,
            setup_globals.diode2,
        )


if setup_globals is None:
    xrpd_plotter = None
else:
    try:
        xrpd_plotter = DemoXrpdPlotter()
    except ImportError:
        xrpd_plotter = None
