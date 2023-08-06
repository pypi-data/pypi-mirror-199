from blissoda.demo.exafs_plotter import exafs_plotter


def bm23_demo(*args, nrepeats=3, **kw):
    for _ in range(nrepeats):
        exafs_plotter.run(*args, **kw)
