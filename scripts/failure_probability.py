from lib.analysis import activity
from lib.analysis import spectrogram
from lib.aux import W7XTimestamp
from matplotlib import pyplot as plt
import numpy as np

foo=activity()
foo.load(src="output/activityMap_Bravo5_last10ms_arithmavg.npy")

#calculate failure frequencies for power intervals:
failed=np.where(np.array(foo.Durations) < 999000000)
ok=np.where(np.array(foo.Durations) >= 999000000)
failedts=[foo.Timestamps[e] for e in failed[0]]
failedts=np.sort(failedts)
failedtsStr=[W7XTimestamp(ts=e).toString() for e in failedts]

data=np.array(foo.U['avg'])
#data=np.array(foo.RF['avg'])
#RF bins
#binarr=np.linspace(500,1000,6)[0:-1]
binarr=np.linspace(78,83,6)
#binarr=np.linspace(38,50,25)
hok=np.histogram(data[ok],bins=binarr)
hfail=np.histogram(data[failed],bins=binarr)
ffail=np.multiply(np.divide(hfail[0],hok[0]),100)
#determine activity value for passed and failed shots in power intervals
#and calculate ratio between the mean values for each power interval
ameans_failed = []
astd_failed = []
test=failed
for e in range(0,len(binarr)-1):
    indices=np.where((data[test] >= binarr[e]) & (data[test] <= binarr[e+1]))
    ameans_failed.append(np.mean(np.array(foo.Activity['normavg'])[indices]))
    astd_failed.append(np.std(np.array(foo.Activity['normavg'])[indices]))
ameans_ok = []
astd_ok = []
test=ok
for e in range(0,len(binarr)-1):
    indices=np.where((data[test] >= binarr[e]) & (data[test] <= binarr[e+1]))
    ameans_ok.append(np.mean(np.array(foo.Activity['normavg'])[indices]))
    astd_ok.append(np.std(np.array(foo.Activity['normavg'])[indices]))
print(hok)
print(hfail)
print(ffail)

xval=[]
yval=[]
for e in range(0,len(binarr)-1):
    steps=np.linspace(binarr[e],binarr[e+1],10)
    xval.extend(steps)
    yval.extend(np.full(len(steps),ffail[e],dtype=np.float32))
f,axarr=plt.subplots(2,sharex=True,figsize=(1600/150,1200/150),dpi=150)
f.subplots_adjust(hspace=.1)
axarr[0].plot(xval,yval,linewidth=2)
axarr[0].yaxis.set_tick_params(labelsize=14)
axarr[0].xaxis.set_tick_params(labelsize=14) 
axarr[0].set_ylabel("Probability of Failure [%]",fontsize=14)
axarr[0].grid(which="major",linestyle=":",color="black")
aratio=np.divide(ameans_failed,ameans_ok)
aratio_x=[]
aratio_y=[]
for e in range(0,len(binarr)-1):
    steps=np.linspace(binarr[e],binarr[e+1],10)
    aratio_x.extend(steps)
    aratio_y.extend(np.full(len(steps),aratio[e],dtype=np.float32))
plt.rc('font', family='serif')
axarr[1].plot(aratio_x,aratio_y,color="red",linewidth=2)
axarr[1].yaxis.set_tick_params(labelsize=14)
axarr[1].xaxis.set_tick_params(labelsize=14) 
axarr[1].set_ylabel(r'$\overline{A}_{failed} : \overline{A}_{passed}$',fontsize=16)
axarr[1].set_xlabel("acceleration voltage [kV]",fontsize=15)
axarr[1].grid(which="major",linestyle=":",color="black")
shifted_binarr=[]
binarrdiff=np.diff(binarr)
for e in range(0,len(binarr)-1):
    shifted_binarr.append(binarr[e]+0.5*binarrdiff[e])
axarr[1].errorbar(x=shifted_binarr,y=aratio,yerr=np.add(astd_ok,astd_failed),fmt='o',ecolor="g",linewidth=2)
f.savefig('PoF_activityratios.png',bbox_inches='tight')

f=plt.figure(figsize=(1600/150,1200/150),dpi=150)
#if correlation between signal and frequency of failure present, a line or graph should appear
#if ratio between mean signal for failed/passed shots and failure frequency is plotted
#if no correlation present only a cloud a data points should be visible
plt.errorbar(x=ffail,y=aratio,yerr=np.add(astd_ok,astd_failed),fmt='o',ecolor="g",linewidth=2)
ax=plt.gca()
ax.yaxis.set_tick_params(labelsize=14)
ax.xaxis.set_tick_params(labelsize=14)
ax.set_ylabel(r'$\overline{A}_{failed} : \overline{A}_{passed}$',fontsize=16)
ax.set_xlabel("Probability of Failure [%]",fontsize=16)
ax.grid(which="major",linestyle=":",color="black")
f.savefig('PoF_vs_activityratio.png',bbox_inches='tight')