from lib.analysis import activity
from lib.analysis import spectrogram
from lib.aux import W7XTimestamp
from matplotlib import pyplot as plt
import numpy as np

foo = activity()
foo.load(src="input/activityMap_Bravo5_last10ms_arithmavg.npy")

# calculate failure frequencies for power intervals:
# failed=np.where(np.array(foo.Durations) < 999000000)
# ok=np.where(np.array(foo.Durations) >= 999000000)
# failedts=[foo.Timestamps[e] for e in failed[0]]
# failedts=np.sort(failedts)
# failedtsStr=[W7XTimestamp(ts=e).toString() for e in failedts]
#
# data=np.array(foo.U['avg'])
# RF bins
# binarr=np.linspace(500,1000,21)
# binarr=np.linspace(78,83,11)
# binarr=np.linspace(38,50,25)
# hok=np.histogram(data[ok],bins=binarr)
# hfail=np.histogram(data[failed],bins=binarr)
# ffail=np.multiply(np.divide(hfail[0],hok[0]),100)
# determine activity value for passed and failed shots in power intervals
# and calculate ratio between the mean values for each power interval
# ameans_failed = []
# test=failed
# for e in range(0,len(binarr)-1):
# 	indices=np.where((data[test] >= binarr[e]) & (data[test] <= binarr[e+1]))
# 	ameans_failed.append(np.mean(np.array(foo.Activity['normavg'])[indices]))
# ameans_ok = []
# test=ok
# for e in range(0,len(binarr)-1):##
# 	indices=np.where((data[test] >= binarr[e]) & (data[test] <= binarr[e+1]))
# 	ameans_ok.append(np.mean(np.array(foo.Activity['normavg'])[indices]))
# print(hok)
# print(hfail)
# print(ffail)
# plt.plot(ffail)
# aratio=np.divide(ameans_failed,ameans_ok)
# plt.plot(aratio,color="red")
# plt.show()
# if correlation between signal and frequency of failure present, a line or graph should appear
# if ratio between mean signal for failed/passed shots and failure frequency is plotted
# if no correlation present only a cloud a data points should be visible
# plt.scatter(ffail,aratio)
# plt.show()

# foo.readBeamParameters(src="input/ESRAY/outsweep_rangeBravo5Experiments.dat")
# foo.setResolution(width=4.44, height=2.5 * 600, dpi=600)
foo.setResolution(width=1900, height=1200, dpi=75)

# foo.plotActivityMap(interpolate=True,rx=100,ry=100,save="activitymap2.png")
# foo.plotActivityMap(interpolate=True,rx=100,ry=100,save="output/AM_last10ms_col_new.eps")
# foo.plotActivityMap3D(save="output/AM3D.png")
# foo.plotPoF3D(save="output/POF3D.png")
# foo.plotPoFInterp(save="output/POFInterp.png")
# foo.plotPoF(save="output/POF.png")
foo.plotPowerVsActivity3(save="powerActivity.eps")
foo.plotPowerVsActivity3(save="powerActivity.png")
# foo.plotAlphaVsActivity(save="output/Duration_Activity_Alpha.png")
# foo.plotAM_DurationVsUVsA(save="output/Duration_Activity.png")
# foo.plotAM_IVsActivityVsAlpha(interpolate=True,rx=100,ry=100,save="output/I_Activity_Alpha_Interp.png")
# foo.plotPowerVsActivity()

# foo=spectrogram()
# foo.load(src='output/shots_overview/')
# foo.create()
# foo.setPlotParameters(dpi=75,widthpx=1900,heightpx=1200,ticksize=16,labelsize=20)
# foo.setPlotParameters(dpi=600,width=4.44,height=2.5,ticksize=5,labelsize=5)
# foo.plotMultiple(save="separate_modes_multiplot.eps")
# foo.plot(tlim=[475,500],save="spectrogram_fullramp.png")
# foo.plot(tlim=[485,500],save="spectrogram_endramp.png")
# foo.plot(tlim=[496,500],flim=[130,143],save="spectrogram_rampend.png")
# foo.plot(tlim=[496,500],flim=[130,136.5])
# foo.plot(tlim=[496,500],flim=[136.5,143])
# foo.setPlotParameters(dpi=75,widthpx=1900,heightpx=1200,ticksize=18,labelsize=20)
# foo.plot(tlim=[0,500],flim=[130,143],save="overview_spectrogram.png")
# foo.plot(tlim=[496,500],flim=[130,143],save="overview_last4ms_spectrogram.png")
# foo.plot()
# foo.plot(tlim=[496,500],flim=[139.9,140.1])
# foo.plot(tlim=[496,500],flim=[142.6,142.8])
# foo.plot(tlim=[496,500],flim=[137.7,137.9])
