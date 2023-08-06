from contextlib import contextmanager

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None

from ..streamline.streamline_scanner import StreamlineScanner as _StreamlineScanner


class StreamlineScanner(_StreamlineScanner):
    def __init__(self):
        super().__init__()
        self._set_parameter_default(
            "detector_name", "p3"
        )  # PilatusCdTe2M or NexusDetector
        self._set_parameter_default("sample_changer_name", "streamline_sc")
        self._set_parameter_default(
            "integration_options",
            {
                "method": "no_csr_ocl_gpu",
                "integrator_name": "sigma_clip_ng",
                "extra_options": {"max_iter": 3, "thres": 0},
                "error_model": "azimuthal",  # hybrid gives weird results
                "nbpt_rad": 5000,
                "unit": "q_nm^-1",
            },
        )

    def _get_scan_metadata(self) -> dict:
        return dict()

    @contextmanager
    def run_context(self):
        setup_globals.shopen()
        with super().run_context():
            yield
