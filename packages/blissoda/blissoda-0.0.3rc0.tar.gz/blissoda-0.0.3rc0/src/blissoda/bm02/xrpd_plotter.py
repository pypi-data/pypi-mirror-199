from ..xrpd_plotter.xrpd_plotter import XrpdPlotter as _XrpdPlotter


class XrpdPlotter(_XrpdPlotter):
    def __init__(self) -> None:
        super().__init__()
        self._set_parameter_default(
            "integration_options",
            {
                "method": "no_csr_cython",
                "nbpt_rad": 2048,
                "unit": "q_nm^-1",
            },
        )
