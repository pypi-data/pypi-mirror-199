from blissoda.demo.xrpd_processor import xrpd_processor


def id31_demo():
    xrpd_processor.enable()
    xrpd_processor.test(npoints=30, expo=1e-2)
