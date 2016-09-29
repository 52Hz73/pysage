from lib.core import W7XAPI
import numpy as np
import time
import matplotlib.pyplot as plt
from lib.analysis import averageShotData
import os
import sys
#import progressbar as pb

start=time.time()
print('Activity Analysis for W7X gyrotron shots')
print('----------------------------------------')
o=W7XAPI(progressbar=False)
o.addChannel(name=['RF'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/8/Rf_B5/scaled/'])
o.addChannel(name=['UBody'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/9/UB_B5/scaled/'])
o.addChannel(name=['UCathode'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/11/UC_B5/scaled/'])
o.addChannel(name=['HPDiode'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/13/IGip_B5/unscaled/'])
o.addChannel(name=['ICathode'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/12/IC_B5/scaled/'])
#o.addChannel(name=['SA'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/1/UB_A5/unscaled/'])
o.addChannel(name=['SA'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/5/IGip_A5/unscaled/'])
#get files in path
if len(sys.argv) < 2:
    raise ValueError('Error: expecting command line argument for input path.')
mypath = sys.argv[1]
files = []
for (dirpath, dirnames, filenames) in os.walk(mypath):
    files.extend(filenames)
    break
avg_data = []
unavg_data = []
counter=0
shots_total = 0
total=len(files)
for filename in files:
    progress = round((float(counter)/float(total))*100,2)
    print('Overall progress:'+str(progress)+' %')
    o.clearShots()
    if os.path.splitext(filename)[1] == '':
        o.searchShots(searchin=['UBody'],mode='match',file=mypath+filename)
        #o.searchShots(searchin=['UBody'],mode='allinrange',file=mypath+filename)
        if len(o.shots) >= 1:
            shots_total += len(o.shots)
            result = averageShotData(o)
            print('Saving intermediate result...')
            print(result['unavg_data']['durations'])
            np.save(mypath + filename + '.npy', dict({'unavg_result':result['unavg_data'],'avg_result':result['avg_data']}))
        counter+=1
        stop=time.time()
        print(str(stop-start) + " seconds elapsed.")
    else:
        continue
print(str(shots_total)+" shots processed in total.")

#widgets = [pb.Percentage(), ' ', pb.Bar(marker='#'), ' ', pb.ETA()]                  
#bar = pb.ProgressBar(widgets=widgets, maxval=len(o.shots)).start()
#counter = 0   
#for shot in o.shots:
#    foo=o.getChannelData(name=['RF'],start=int(shot['begin']),stop=int(shot['end']))     
#    plt.plot(foo['RF']['dimensions'],foo['RF']['values']) 
#    counter += 1
#    bar.update(counter)
#bar.finish()     
#for shot in o.errPosEdges:
#    #foo=o.getChannelData(name=['RF'],start=int(shot['begin']),stop=int(shot['end']))     
#    #plt.plot(foo['RF']['dimensions'],foo['RF']['values'])                       
#    plt.plot([shot,shot],[0,1000],'r-')
#    #plt.plot([shot['end'],shot['end']],[np.min(foo['RF']['values']),np.max(foo['RF']['values'])],'r-')
#plt.show()
stop=time.time()
print(str(stop-start) + " seconds elapsed in total.")