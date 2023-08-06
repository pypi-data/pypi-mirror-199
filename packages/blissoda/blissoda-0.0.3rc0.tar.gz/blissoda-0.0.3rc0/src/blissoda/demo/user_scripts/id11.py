try:
    from bliss import current_session
except ImportError:
    current_session = None

from blissoda.demo.id11 import xrpd_processor


def id11_demo():
    xrpd_processor.enable(current_session.env_dict["difflab6"])
    xrpd_processor.retry_timeout = 600
    xrpd_processor.test(npoints=30, expo=1e-2)
