import numpy as np
import matplotlib.pyplot as plt
from activity_plot import rf_norm_activity2, tavg_activity

def averageShotData(oW7XAPI):
    maxU = []
    maxIc = []
    Ic = []
    avg_activity = []
    tavg_activity = []
    rfpower = []
    rf_norm_activity = []
    rf_norm_activity2 = []
    durations = []
    max_activity = []
    min_activity = []
    activity_decay_time = []   
    total = len(oW7XAPI.shots)
    counter=0
    print('Activity analysis...')
    if len(oW7XAPI.matchedShots) > 0:
        tosearch = oW7XAPI.matchedShots
    else:
        tosearch = oW7XAPI.shots
    for obj in tosearch:
        #get working point
        datUb = oW7XAPI.getChannelData(name=['UBody'],start=obj['begin'],stop=obj['end'])
        datUc = oW7XAPI.getChannelData(name=['UCathode'],start=obj['begin'],stop=obj['end'])
        maxU.append(np.max(datUb['UBody']['values'])+np.max(datUc['UCathode']['values']))
        datIc = oW7XAPI.getChannelData(name=['ICathode'],start=obj['begin'],stop=obj['end'])
        maxIc.append(np.max(datIc['ICathode']['values']))
        t1=np.min(datIc['ICathode']['dimensions'])
        t2=np.max(datIc['ICathode']['dimensions'])       
        Ic.append(float(1.0/(t2-t1))*np.trapz(datIc['ICathode']['values'],datIc['ICathode']['dimensions']))
        #get time average for activity   
        datHPDiode = oW7XAPI.getChannelData(name=['HPDiode'],start=obj['begin'],stop=obj['end'])     
        t1=np.min(datHPDiode['HPDiode']['dimensions'])
        t2=np.max(datHPDiode['HPDiode']['dimensions'])       
        tavg_activity.append(float(1.0/(t2-t1))*np.trapz(datHPDiode['HPDiode']['values'],datHPDiode['HPDiode']['dimensions']))        
        avg_activity.append(np.mean(datHPDiode['HPDiode']['values']))
        max_activity.append(np.max(datHPDiode['HPDiode']['values']))
        min_activity.append(np.min(datHPDiode['HPDiode']['values']))
        
        #determine time for activity decay
        #calculate moving time average for diode signal (low pass filter like)
        #using convolution with identity
        #equals 50ms for 25kHz sampling frequency
        #window_size = 1250 
        #moving_avg_activities = np.convolve(datHPDiode['HPDiode']['values'],np.ones(window_size)/float(window_size),'same')
        #plt.plot(datHPDiode['HPDiode']['dimensions'],datHPDiode['HPDiode']['values'],'b')
        #plt.plot(datHPDiode['HPDiode']['dimensions'],moving_avg_activities,'r')
        #plt.show()
        #try to determine decay time - not clearly possible
        #min_mavg = np.min(moving_avg_activities)
        #max_mavg = np.max(moving_avg_activities)
        #amp_mavg = (max_mavg - min_mavg)
        #decay_index = np.where(moving_avg_activities < )
        
        #get rf power
        datRF = oW7XAPI.getChannelData(name=['RF'],start=obj['begin'],stop=obj['end'])
        rfpower.append(np.mean(datRF['RF']['values']))
        #get normalized activity
        rf_norm_activity.append(float(avg_activity[-1] / rfpower[-1])) 
        rf_norm_activity2.append(float(tavg_activity[-1] / rfpower[-1]))
        durations.append(obj['duration']/1e6)
        counter+=1
        progress = round((float(counter)/float(total))*100,2)
        print('Progress:'+str(progress)+" % ",end='\r')
        
        #plt.plot(datHPDiode['HPDiode']['dimensions'],datHPDiode['HPDiode']['values'])
        #plt.show()
        #plt.plot(datRF['RF']['dimensions'],datRF['RF']['values'])
        #plt.show()
        #plt.plot(datUb['UBody']['dimensions'],datUb['UBody']['values'])
        #plt.show()
        #plt.plot(t_activity_chunks)
        #plt.show()
       
    unavg_data = dict({'durations':durations,'maxU':maxU,'maxIc':maxIc,'Ic':Ic,'tavg_activity':tavg_activity,'avg_activity':avg_activity,'rfpower':rfpower,'rf_norm_activity2':rf_norm_activity2,'rf_norm_activity':rf_norm_activity})
    avg_data = dict({'avg_maxU':np.mean(maxU),'avg_maxIc':np.mean(maxIc),'avg_Ic':np.mean(Ic),'avg_avg_activity':np.mean(avg_activity),'avg_rfpower':np.mean(rfpower),'avg_rf_norm_activity':np.mean(rf_norm_activity)})
    return dict({'unavg_data':unavg_data,'avg_data':avg_data})