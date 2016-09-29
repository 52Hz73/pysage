import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
import os
import sys

if len(sys.argv) < 2:
    raise ValueError('Error: expecting command line argument for input path.')
mypath = sys.argv[1]
files = []
for (dirpath, dirnames, filenames) in os.walk(mypath):
    files.extend(filenames)
    break
total=len(files)
counter=0
activityData = []
#load preprocessed files (created with activity.py in python3
print("Loading numpy files...")
for filename in files:
    if os.path.splitext(filename)[1] == ".npy":   
        activityData.append(np.load(dirpath+filename).item())
#aggregate data
Ic = []
Umax = []
rfpower = []
avg_activity = []
maxIc = []
tavg_activity = []
rf_norm_activity = []
rf_norm_activity2 = []
durations = []
for elem in activityData:
    Ic.extend(elem['unavg_result']['Ic'])
    Umax.extend(elem['unavg_result']['maxU'])
    avg_activity.extend(elem['unavg_result']['avg_activity'])
    tavg_activity.extend(elem['unavg_result']['tavg_activity'])
    rfpower.extend(elem['unavg_result']['rfpower'])
    rf_norm_activity.extend(elem['unavg_result']['rf_norm_activity'])
    rf_norm_activity2.extend(elem['unavg_result']['rf_norm_activity2'])
    durations.extend(elem['unavg_result']['durations'])

#plt.plot([(avg_activity[i]/tavg_activity[i]) for i in range(0,len(avg_activity))])
#plt.show()
#plt.scatter(rfpower,avg_activity,c='blue')
#plt.scatter(rfpower,tavg_activity,c='red')
#plt.show()

#plot activity map
cm = plt.cm.get_cmap('hot')
fig = plt.figure(figsize=(1600/75, 1200/75), dpi=75)
sc=plt.scatter(x=Umax,y=Ic,c=tavg_activity, vmin=-1000, vmax=1000, s=15, cmap=cm)
plt.colorbar(sc,label='mean diode signal [mV]')
#plt.axis([78,84,38,50])
plt.grid(True)
plt.title('Activity map',fontsize=28)
plt.xlabel('acceleration voltage [kV]',fontsize=20)
plt.ylabel('cathode current [A]',fontsize=20)
matplotlib.rcParams['xtick.labelsize'] = 20
matplotlib.rcParams['ytick.labelsize'] = 20
plt.show()
fig.savefig('activity_map.png')

#plot rf output power vs. normalized diode signal (activity)
#fig = plt.figure(figsize=(1600/75, 1200/75), dpi=75)
#plt.axis([500,np.max(rfpower),-2,2])
#plt.title('RF Power vs. RF normalized activity',fontsize=28)
#plt.scatter(x=rfpower,y=rf_norm_activity, s=20)
#plt.xlabel('RF output power [kW]',fontsize=20)
#plt.ylabel('normalized activity [a.u.]',fontsize=20)
#matplotlib.rcParams['xtick.labelsize'] = 20
#matplotlib.rcParams['ytick.labelsize'] = 20
#plt.grid(True)
#plt.show()
#fig.savefig('rfpower_vs_norm_activity.png')