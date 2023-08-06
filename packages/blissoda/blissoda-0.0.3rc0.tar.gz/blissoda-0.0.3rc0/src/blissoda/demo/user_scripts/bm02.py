from blissoda.demo.xrpd_plotter import xrpd_plotter


def bm02_demo(*args, **kw):
    xrpd_plotter.enable()
    xrpd_plotter.test(*args, **kw)
