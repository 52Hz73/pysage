from lib.analysis import activity
from lib.analysis import spectrogram
from lib.aux import W7XTimestamp
from matplotlib import pyplot as plt
import numpy as np
import sys

foo = spectrogram()
foo.load(src=sys.argv[1])
# foo.create(sync='modeloss')
foo.create(sync=sys.argv[2])
# foo.setPlotParameters(dpi=600,width=4.44,height=2.5,ticksize=5,labelsize=5)
# foo.setPlotParameters(dpi=150, widthpx=1600, heightpx=1200, ticksize=14, labelsize=20)
foo.setPlotParameters(dpi=150, width=4.44, height=2.5, ticksize=14, labelsize=20)
# foo.plot(tlim=[0, 500])
# foo.plotMultiple(save="separate_modes_multiplot_broad_sync.png")
foo.plot1DSpectrumAt(t=498000000)
a = foo.getAmplitudeVsTime(f1=133.9E9, f2=140.5E9)
plt.scatter(a[0], a[1])
plt.show()
