from lib.core import W7XAPI
import numpy as np
import time
import matplotlib.pyplot as plt
#import progressbar as pb

start=time.time()
print('PySAGE')
print('----------------------------')
o=W7XAPI(progressbar=False)
o.addChannel(name=['RF'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/8/Rf_B5/scaled/'])
o.addChannel(name=['UBody'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/9/UB_B5/scaled/'])
o.addChannel(name=['HPDiode'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/13/IGip_B5/unscaled/'])
o.addChannel(name=['ICathode'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/12/IC_B5/scaled/'])
o.addChannel(name=['SA'],url=['codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/1/UB_A5/unscaled/'])
o.searchShots(searchin=['UBody'],mode='match',file='input/test')
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
print(str(stop-start) + " seconds elapsed.")