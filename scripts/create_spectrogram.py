from lib.analysis import activity
from lib.analysis import spectrogram
from lib.aux import W7XTimestamp
from matplotlib import pyplot as plt
import numpy as np
import sys

foo=spectrogram()
foo.load(src=sys.argv[1])
#foo.create(sync='modeloss')
foo.create(sync=sys.argv[3])
foo.setPlotParameters(dpi=150,widthpx=1600,heightpx=1200,ticksize=14,labelsize=20)
foo.plot(tlim=[0,500],save=sys.argv[2])
#foo.plotMultiple(save="separate_modes_multiplot_broad_sync.png")
#foo.plotMultiple(save=sys.argv[2])
