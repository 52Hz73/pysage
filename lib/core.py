#external imports
import matplotlib
import numpy as np
import requests
import json
import os, sys, time, datetime, codecs
import urllib.parse
import matplotlib.pyplot as plt

#internal imports
from lib.aux import progressBar, arrayHelper

"""
Module description:
module core contains all base functions underneath the visible GUI of the program

Author:
Fabian Wilde, IPP HGW

Date:
August 2016
"""

""" 
Description:
class W7XAPI encapsulates all methods to have general access to 
the W7X data aquisition database

Author: 
Fabian Wilde, IPP HGW

Date:
August 2016
"""

class W7XAPI(object):
    # constructor
    def __init__(self, **kwargs):
        
        self.channels = []
        self.intervals = dict()
        self.timestamps = dict()
        self.shots = []
        self.matchedShots = []        
        self.errPosEdges = []
        self.errNegEdges = []
        self.timestampFile = ''        
        
        if 'baseurl' in kwargs.keys():
            self.baseurl = kwargs['baseurl']
        else:
            self.baseurl = 'http://archive-webapi.ipp-hgw.mpg.de/ArchiveDB/'            
        
        # string specifying format for timestamp conversion from/to string
        # ex.: 15-07-2016 10:41:26,411
        if 'format' in kwargs.keys():
            self.formatstr = kwargs['format'] 
        else:            
            self.formatstr = "%d-%m-%Y %H:%M:%S,%f"
        # for shot recognition - time before detected shot begins in nanoseconds
        if 'tbefore' in kwargs.keys():
            self.timeBefore = kwargs['tbefore']
        else:
            self.timeBefore = 250000
        if 'tafter' in kwargs.keys():
            self.timeAfter = kwargs['tafter']
        else:
            self.timeAfter = 250000
        if 'searchmode' in kwargs.keys():
            self.searchMode = kwargs['searchmode']
        else:
            self.searchMode = 'allinrange'
        # default method for shot detection is edge pair detection (derivative)
        if 'method' in kwargs.keys():            
            self.detectMethod = kwargs['method']
        else:
            self.detectMethod = 'edges'
        if 'ttol' in kwargs.keys():
            self.timeTolerance = kwargs['ttol']
        else:
            self.timeTolerance = 2000000000
        if 'stol' in kwargs.keys():
            self.sampleTolerance = kwargs['stol']
        else:
            self.sampleTolerance = 1
        if 'toldev' in kwargs.keys():
            self.toleratedDeviance = kwargs['toldev']
        else:
            self.toleratedDeviance = 0.1    
    
    # send a get request to given url        
    def request(self, **kwargs):
        header = {'Accept':'application/json'}
        if not 'url' in kwargs:
            raise ValueError(' input argument dictionary is missing necessary keyword ''url''.')
        if 'params' in kwargs:
            params = kwargs['params']
        else:
            params = []
        try:
            r = requests.get(kwargs['url'], headers=header, params=params)
        except:     
            print(' Could not connect to given ressource URL.')
            exit(2)
        try:
            json_data = r.json()
        except ValueError:
            print(' Invalid response for GET request by given ressource URL.')
            exit(3)  
            
        return json_data 
                 
    # gives sub paths for given ressource url 
    def list(self, *kwargs):
        json_data = self.request(url=(self.baseurl + kwargs[0]))
        if '_links' in  json_data.keys():
            if 'children' in json_data['_links'].keys():
                subdirs = []
                # iterate over dictionary in Python 2.x
                for elem in json_data['_links']['children']:  
                    foo = elem['href'].split('/')                                 
                    if len(foo[-1]) == 0:
                        subdirs.append(foo[-2])
                    else:
                        subdirs.append(foo[-1])
                return subdirs
        else:
            return []
        
    # adds a channel (name,url) pair to W7XAPI object        
    def addChannel(self, **kwargs):
        if ('name' in kwargs.keys()) & ('url' in kwargs.keys()):
            absURLs = False
            if 'absolute' in kwargs.keys():
                if kwargs['absolute'] == 'True':
                    absURLs = True            
            if len(kwargs['name']) == len(kwargs['url']):
                # check for double entries
                for elem in kwargs['name']:                    
                    if not elem in [i['name'] for i in self.channels]:                                              
                        if absURLs:
                            url = kwargs['url'][kwargs['name'].index(elem)]                                    
                        else:
                            url = self.baseurl + kwargs['url'][kwargs['name'].index(elem)] 
                        
                        self.channels.append(dict({'name':elem, 'url':url}))                                                   
                    else:
                        print(elem + " not added since it would result in double entry.")
            else:
                raise ValueError(' number of entries for url and name are not equal.')            
        else:
            raise ValueError(' missing keys in input argument dictionary.') 
    
    # deletes channel
    def rmChannel(self, **kwargs):
        if 'name' in kwargs.keys():
            if len(kwargs['name']) > 0:
                for elem in kwargs['name']:
                    if elem in [i['name'] for i in self.channels]:
                        pos = [i['name'] for i in self.channels].index(elem)
                        del self.channels[i]                     
                    else:
                        print('Warning: channel name ' + elem + ' not found in channel list.')
            else:
                raise ValueError(' given list for channel names is empty.')
        else:
            raise ValueError(' missing key ''name'' in input argument dictionary.')

    # clears channel list                
    def clearChannels(self):
        self.channels = {}

    # get data for given channels within specified time interval                                                    
    def getChannelData(self, **kwargs):   
        needed = ['start', 'stop']
                 
        for elem in needed:
            if not elem in kwargs.keys():
                raise ValueError(' missing key ' + elem + ' in input argument dictionary.')
       
        if 'name' in kwargs.keys():
            channels2download = kwargs['name']
        else:
            channels2download = [i['name'] for i in self.channels]  
        
        channelnames = [i['name'] for i in self.channels]              
            
        if 'format' in kwargs.keys():
            formatstr = kwargs['format']
        else:
            formatstr = self.formatstr 
            
        result = dict()
    
        # check channel names
        for elem in channels2download:       
            if elem in [i['name'] for i in self.channels]:
                result.update(dict({elem:[]}))                             
                resurl = self.channels[channelnames.index(elem)]['url'] + '_signal.json' 
                
                #if not (type(kwargs['start']) is int) | (type(kwargs['start']) is long) | (type(kwargs['start']) is np.int64):
                if not (type(kwargs['start']) is int) | (type(kwargs['start']) is np.int64):
                    tsStart = datetime.datetime.strptime(kwargs['start'], formatstr)
                else:
                    tsStart = kwargs['start']
                    
                if type(kwargs['start']) is np.int64:
                    tsStart = int(kwargs['start'])
                    
                #if not (type(kwargs['stop']) is int) | (type(kwargs['stop']) is long) | (type(kwargs['stop']) is np.int64):
                if not (type(kwargs['stop']) is int) | (type(kwargs['stop']) is np.int64):
                    tsStop = datetime.datetime.strptime(kwargs['stop'], formatstr)
                else:
                    tsStop = kwargs['stop']
                    
                if type(kwargs['stop']) is np.int64:
                    tsStop = int(kwargs['stop'])
                 
                json_data = self.request(url=resurl, params={'from':tsStart, 'upto':tsStop})                                                              
                if type(json_data) == type([]):
                    print('No data available for channel ' + elem + '\n in specified time range \n ' + datetime.datetime.utcfromtimestamp(kwargs['start'] / 1e9) + ' to ' + datetime.datetime.utcfromtimestamp(kwargs['stop'] / 1e9))          
                elif 'message' in json_data:
                    print(json_data['message'])
                else:
                    result.update(dict({elem:json_data}))                
            else:
                print('Warning: omitting channel with name ' + elem + ' since not found in channel list.')
        return result
    
    # get intervals with available data
    def getIntervals(self, **kwargs):            
        needed = ['start', 'stop']
                 
        for elem in needed:
            if not elem in kwargs.keys():
                raise ValueError(' missing key ' + elem + ' in input argument dictionary.')
            
        if 'name' in kwargs.keys():
            channelnames = kwargs['name']
        else:
            channelnames = [i['name'] for i in self.channels]                    
            
        if 'format' in kwargs.keys():
            formatstr = kwargs['format']
        else:
            formatstr = self.formatstr                
                                                   
        for elem in channelnames:
            print("Requesting intervals with data available for channel '" + elem + "'...")
            result = []
            if elem in [i['name'] for i in self.channels]:                   
                resurl = self.channels[channelnames.index(elem)]['url']
                   
                pagecounter = 1
                finished = 0
            
                while finished == 0:                   
                    json_data = self.request(url=resurl, params={'page':pagecounter,'filterstart':kwargs['start'], 'filterstop':kwargs['stop']})
                    #json_data = self.request(url=resurl, params={'page':100,'filterstart':1468454400000000000, 'filterstop':146854079999999999})
                                                 
                    if not type(json_data) == 'list':
                        if '_links' in json_data:
                            if 'children' in json_data['_links']: 
                                # process url strings to extract interval timestamps
                                for urlstr in [i['href'] for i in json_data['_links']['children']]:
                                    # parse url string
                                    #par = urlparse.parse_qs(urlparse.urlparse(urlstr).query)
                                    par = urllib.parse.parse_qs(urllib.parse.urlparse(urlstr).query)
                                    # convert timestamp to formatted string
                                    dtFrom = datetime.datetime.utcfromtimestamp(int(par['from'][0]) / 1e9)
                                    strFrom = dtFrom.strftime(formatstr)
                                    # convert timestamp to formatted string
                                    dtUpto = datetime.datetime.utcfromtimestamp(int(par['upto'][0]) / 1e9)
                                    strUpto = dtUpto.strftime(formatstr)
                                    
                                    #elemdict = dict({'from':long(par['from'][0]), 'upto':long(par['upto'][0]), 'strFrom':strFrom, 'strUpto':strUpto}) 
                                    elemdict = dict({'from':int(par['from'][0]), 'upto':int(par['upto'][0]), 'strFrom':strFrom, 'strUpto':strUpto})  
                                    
                                    if len(result) > 0:
                                        #check if interval has been already added to the list
                                        from_tmp_arr = np.array([i['from'] for i in result])
                                        upto_tmp_arr = np.array([i['upto'] for i in result])
                                        check = np.where(int(par['from'][0]) == from_tmp_arr)[0]                                    
                                        check2 = np.where(int(par['upto'][0]) == upto_tmp_arr)[0]                                                                                             
                                        
                                        if not len(check) > 0:
                                            result.append(elemdict)                                             
                                        else:                                        
                                            finished = 1
                                            break
                                    else:
                                        result.append(elemdict)
                                
                                if len(result) > 0:
                                    self.intervals.update(dict({elem:result}))
                                    pagecounter += 1
                                else:
                                    self.intervals.update(dict({elem:[]}))
                                    finished = 1                                       
                            else:
                                finished = 1
                        else:
                            finished = 1
                    else:
                        finished = 1
                    
                if len(self.intervals[elem]) > 0:
                    #reverse element order
                    self.intervals.update(dict({elem:result[::-1]}))
                    print(str(len(self.intervals[elem])) + " intervals available.")
                else:
                    print("No available intervals found for channel '"+elem+"'.")
            else:
                print('Warning: omitting channel with name ' + elem + ' since not found in channel list.')                                         
            
        return self.intervals    
                               
    def clearIntervals(self):
        self.intervals = dict()
        
    def clearTimestamps(self):
        self.timestamps = dict()   
        self.timestampFile = ''
        
    # reads in text file with timestamps for later processing        
    def readTimestampFile(self, **kwargs):
        if not 'file' in kwargs.keys():
            raise ValueError(' input argument dictionary is missing expected keyword ''file''.')
        
        self.timestampFile = kwargs['file']
        print('Reading file ' + kwargs['file'] + '...')
        with open(kwargs['file']) as f:
            content = f.read().splitlines()
        
        if not 'skipevery' in kwargs.keys():
            skipevery = 1
        else:
            skipevery = kwargs['skipevery']
            
        if not 'skip' in kwargs.keys():
            skip = 0
        else:
            skip = kwargs['skip']
            
        if 'format' in kwargs.keys():
            formatstr = kwargs['format']
        else:
            formatstr = self.formatstr
            
        tsdata = dict()
        numTimestamps = [];
        strTimestamps = [];
        auxData = [];        
            
        for line_num in range(skip, len(content), skipevery):
            line = content[line_num]            
            # try conversion to numeric timestamp, if it fails, no valid timestamp representation
            # according to string containing timestamp string format definition
            try:               
                dtobj = datetime.datetime.strptime(line, formatstr)                
            except ValueError:
                # print('Warning: Line ' +str(line_num)+ ' does not contain a valid convertable timestamp.')
                auxData.append(line);
                continue                
            numts = ((dtobj - datetime.datetime(1970, 1, 1, 0, 0, 0)).total_seconds() * 1E9)
            numTimestamps.append(int(numts))
            strTimestamps.append(line)
        tsdata.update({'numeric':numTimestamps, 'string':strTimestamps, 'aux':auxData})
        self.timestamps = tsdata
        return tsdata            
        
    # clears list with previously detected shots
    def clearShots(self):
        self.shots = []  
        self.matchedShots = []
        self.errPosEdges = []
        self.errNegEdges = []
        
    # saves shots in file with combined channel data of the shot
    def saveShotData(self, **kwargs):              
        if not len(self.shots) > 0:
            raise ValueError("no shots available to be saved. Search for shots first.")
        
        if 'name' in kwargs.keys():
            channelnames = kwargs['name']
        else:
            channelnames = [i['name'] for i in self.channels]
        
        # if no destination path given, use actual working directory                  
        if 'ptype' in kwargs.keys():
            ptype = kwargs['ptype']
        else:
            ptype = 'relative' 
            
        if 'dest' in kwargs.keys():
            if ptype == 'relative':
                destination = os.getcwd() + os.sep + kwargs['dest']
            else:
                destination = kwargs['dest']
        else:
            destination = os.getcwd() 
            
        if 'progressbar' in kwargs.keys():
            if not kwargs['progress'] in [True, False]:
                raise ValueError(" expected boolean for input argument 'progressbar'.")
            self.progressbar = kwargs['progress']
        else:
            self.progressbar = True

        #init progressbar
        if self.progressbar:
            bar = progressBar(total=len(channelnames))
                     
        for shot in self.shots:
            shotResult = dict()                                    
                         
            for channel in channelnames:
                # take into account the time before and after shot (prepend/append extra time)                        
                shotData = self.getChannelData(name=[channel], start=shot['begin'] - self.timeBefore, stop=shot['end'] + self.timeAfter)                
                if not len(shotData) == 0:
                    shotResult.update(shotData)
                counter += 1
                if self.progressbar:
                    #update progressbar
                    bar.update(counter)
            if not len(shotResult) == 0:
                # save file for shot with channel data              
                np.save(destination + os.sep + 'shot_' + str(shot['begin']) + '_' + str(shot['end']) + '.npy', shotResult)
                # to recover dict
                # foo=np.load(...)
                # then
                # dict = foo.item()
        if self.progressbar:        
            bar.finish()            
            
    #Warning: can consume a lot of RAM!
    def getShotData(self, **kwargs):
        if not len(self.shots) > 0:
            raise ValueError("no shots available to be saved. Search for shots first.")
        
        if 'name' in kwargs.keys():
            channelnames = kwargs['name']
        else:
            channelnames = [i['name'] for i in self.channels]
            
        if 'progressbar' in kwargs.keys():
            if not kwargs['progress'] in [True, False]:
                raise ValueError(" expected boolean for input argument 'progressbar'.")
            self.progressbar = kwargs['progress']
        else:
            self.progressbar = True
                    
        #init progressbar
        if self.progressbar:
            counter=0
            bar = progressBar(total=len(channelnames))
                     
        totalResult = []
        for shot in self.shots:
            shotResult = dict()                                    
                         
            for channel in channelnames:
                # take into account the time before and after shot (prepend/append extra time)                        
                shotData = self.getChannelData(name=[channel], start=shot['begin'] - self.timeBefore, stop=shot['end'] + self.timeAfter)                
                if not len(shotData) == 0:
                    shotResult.update(shotData)
                                    
                if self.progressbar:            
                    #update progressbar
                    counter += 1
                    bar.update(counter)
            #append dict with shotData to array
            totalResult.append(shotResult)
           
        if self.progressbar:        
            bar.finish()            
        
        #return array of dicts containing the data for all defined channels for the shot
        return totalResult
    
    # search for shots in channel data
    def searchShots(self, **kwargs):
        if not 'searchin' in kwargs.keys():
            print('Warning: no channel name given to search in. Using first defined channel.')
            searchin = self.channels[0]
        else:
            if (type(kwargs['searchin']) == type([])) & (len(kwargs['searchin']) > 1):
                raise ValueError("too much arguments given for parameter 'searchin'. Only one is expected.")
            else:
                if not kwargs['searchin'][0] in [i['name'] for i in self.channels]:
                    raise ValueError('given channel name is not defined.')
                else:
                    pos = [i['name'] for i in self.channels].index(kwargs['searchin'][0])
                    searchin = self.channels[pos]                          
                    
        if 'name' in kwargs.keys():
            channelnames = kwargs['name']
        else:
            channelnames = [i['name'] for i in self.channels]                                                
                
        if 'mode' in kwargs.keys():
            searchMode = kwargs['mode']
        else:
            searchMode = self.searchMode
        
        if 'method' in kwargs.keys():
            detectMethod = kwargs['method']
        else:
            detectMethod = self.detectMethod
            
        # minimum shot length set to 1 millisecond
        if 'minlen' in kwargs.keys():
            minlen = int(kwargs['minduration'])
        else:
            minlen = 1000000
            
        if 'ttol' in kwargs.keys():
            ttol = kwargs['ttol']
        else:
            ttol = self.timeTolerance
            
        if 'toldev' in kwargs.keys():
            toldev = kwargs['toldev']
        else:
            toldev = self.toleratedDeviance
            
        if 'stol' in kwargs.keys():
            stol = kwargs['stol']
        else:
            stol = self.sampleTolerance
            
        if 'tbefore' in kwargs.keys():
            tbefore = kwargs['tbefore']
        else:
            tbefore = self.timeBefore
            
        if 'tafter' in kwargs.keys():
            tafter = kwargs['tafter']
        else:
            tafter = self.timeAfter
            
        if 'progressbar' in kwargs.keys():
            if not kwargs['progress'] in [True, False]:
                raise ValueError(" expected boolean for input argument 'progressbar'.")
            self.progressbar = kwargs['progress']
        else:
            self.progressbar = True
            
        if searchMode == 'allinrange':
            if not (('start' in kwargs.keys()) & ('stop' in kwargs.keys())) | ('file' in kwargs.keys()):
                raise ValueError("either a file needs to be specified with parameter 'file' or a time range with parameters 'start' and 'stop'.")
        
            self.clearTimestamps()
            self.clearIntervals()
                
            if 'file' in kwargs.keys():
                # read in file with timestamps
                self.readTimestampFile(file=kwargs['file'])
                # get available intervals in between first and last timestamp in file
                self.getIntervals(name=[searchin['name']], start=self.timestamps['numeric'][0], stop=self.timestamps['numeric'][-1])
            
            if ('start' in kwargs.keys()) & ('stop' in kwargs.keys()):
                self.getIntervals(name=[searchin['name']], start=kwargs['start'], stop=kwargs['stop'])
                                            
            # download intervals
            # define NumPy array for faster processing and more efficient memory usage
            rawData_values = []
            rawData_dimensions = []
              
            print("Download search channel data...\n")  
            
            #init progressbar
            if self.progressbar:
                bar = progressBar(total=len(self.intervals[searchin['name']]))
                counter = 0
            if not searchin['name'] in self.intervals.keys():          
                print("Warning: no intervals with data available for channel '"+searchin['name']+"'. Nothing to do then.")
                exit(0)
            for elem in self.intervals[searchin['name']]:                            
                res = self.getChannelData(name=[searchin['name']], start=elem['from'], stop=elem['upto'])
                rawData_values.append(np.array(res[searchin['name']]['values']))
                rawData_dimensions.append(np.array(res[searchin['name']]['dimensions']))
                # np.array(rawData[-1]['values']).tofile(searchin['name']+str(elem['from'])+'_'+str(elem['upto'])+"_values.bin")         
                # np.array(rawData[-1]['dimensions']).tofile(searchin['name']+str(elem['from'])+'_'+str(elem['upto'])+"_dimensions.bin")
                if self.progressbar:
                    counter += 1                                                    
                    bar.update(counter)
            
            if self.progressbar:        
                bar.finish()
            
            # identify edge pairs in signal
            print("Detecting edges...")   
            
            #init progressbar
            if self.progressbar:
                bar = progressBar(total=len(rawData_values))
                counter = 0                                 
            
            resPosEdgesTs = np.array([], dtype=np.int64)
            resNegEdgesTs = np.array([], dtype=np.int64)             
            
            # prepare data 
            for j in range(0, len(rawData_values)):
                elem = rawData_values[j]            
                d = np.diff(elem)
                dmean = np.mean(d)
                dstd = np.std(d)                                                                
                dthreshold = np.abs(dmean) + 5 * dstd
                # determine edges
                edges = np.where(np.abs(d) >= dthreshold)[0]
                posEdges = edges[np.where(d[edges] >= 0)[0]]
                negEdges = edges[np.where(d[edges] < 0)[0]]                    
                    
                if posEdges.size:            
                    # analyze which data points belong to same edge
                    foo = arrayHelper.getUniformAreas(posEdges, stol)                  
                    # take value with middle position
                    foo2 = np.array([arrayHelper.getMiddleValue(i) for i in foo])                        
                    # obtain time stamps for edges
                    posEdgesTs = np.array(rawData_dimensions[j][foo2], dtype=np.int64)                        
                    # save result in array
                    resPosEdgesTs = np.concatenate([resPosEdgesTs, posEdgesTs])                                 
       
                if negEdges.size:                                
                    # analyze which data points belong to same edge
                    foo = arrayHelper.getUniformAreas(negEdges, stol)                 
                    # take value with middle position
                    foo2 = np.array([arrayHelper.getMiddleValue(i) for i in foo])                        
                    # obtain time stamps for edges
                    negEdgesTs = np.array(rawData_dimensions[j][foo2], dtype=np.int64)           
                    # save result in array                
                    resNegEdgesTs = np.concatenate([resNegEdgesTs, negEdgesTs]) 
                    
                if self.progressbar:
                    counter += 1                                                    
                    bar.update(counter)  
            
            if self.progressbar:
                bar.finish()                                                                                                              
            
            print("Assembling shots...")               
            
            #init progressbar
            if self.progressbar:
                bar = progressBar(total=len(resPosEdgesTs))
                counter = 0               
                        
            for pos_edge in resPosEdgesTs:                    
                #calculate distances between actual positive edge and all detected negative edges
                distances = np.array([(neg_edge - pos_edge) for neg_edge in resNegEdgesTs])
                pos_distances_index = np.where(distances >= 0)
                pos_distances = distances[pos_distances_index]
                #if no positive found for actual positive edge, sort it out
                if len(pos_distances) == 0:
                    self.errPosEdges.append(pos_edge)
                    #continue with next positive edge
                    continue
                min_distance = np.min(pos_distances)
                min_distance_index = np.where(pos_distances == min_distance)[0]
            
                #if detected shot shorter than minimum defined length, use next positive edge, if any
                if (min_distance < minlen) & (len(pos_distances) > 1): 
                    foo=pos_distances.tolist()
                    foo.pop(min_distance_index)
                    min_distance = np.min(foo)
                    min_distance_index = np.where(pos_distances == min_distance)                                                            
                    
                candidate_index = np.where(distances == min_distance)[0]
                candidate = resNegEdgesTs[candidate_index] 
                cand_distances = distances[candidate_index]                                                                                                               
         
                if len(candidate) > 1:
                    print("Warning: More than one possible candidate found for edge with timestamp '" + str(pos_edge) + "'")
                    self.errEdges.append({'reason':'ambigous','timestamp':pos_edge})
                elif len(candidate) == 0:
                    print("Warning: No possible candidate found for edge with timestamp '" + str(pos_edge) + "'")
                    self.errEdges.append({'reason':'singular','timestamp':pos_edge})
                else:      
                                    
                    candidate = candidate[0]                                                    
                    
                    #test if there is another positive edge between the actual positive edge and the assigned negative edge
                    #if so, the actual positive edge probably has been falsely detected
                    #sufficient to test if the following positive edge appears before the assigned negative edge
                    pos_edge_index = np.where(pos_edge == resPosEdgesTs)[0]
                    #if there is a next positive edge
                    if (pos_edge_index+1) <= (len(resPosEdgesTs)-1):
                    #check if next positive edge comes after the candidate negative edge
                        if candidate > resPosEdgesTs[pos_edge_index+1]:
                            #if so, actual positive edge is potentially a detection failure
                            #add to list of false positive edges
                            self.errPosEdges.append(pos_edge)
                            #continue with next positive edge
                            continue
                        else:                                    
                            #remove positive edge from list
                            resPosEdgesTs=np.delete(resPosEdgesTs,np.where(resPosEdgesTs == pos_edge))
                            #remove negative edge from list
                            resNegEdgesTs=np.delete(resNegEdgesTs,candidate_index)                                                        
                            # save result for detected shot                                                  
                            self.shots.append({'begin':pos_edge, 'end':candidate, 'duration':cand_distances[0]})
                            
                if self.progressbar:
                    counter += 1                                                    
                    bar.update(counter)  
            
            if self.progressbar:
                bar.finish()                                                                                                                                                                                                                                 
                   
            #create histogram
            shotDurations = [shot['duration'] for shot in self.shots]
            hist = np.histogram(shotDurations)
            shotDev = np.std(shotDurations)
            shotMean=np.mean(shotDurations)            
            frequencies = hist[0]
            bins = hist[1]                           
            
            #sort out invalid shots assuming that desired shot length is the most frequent
            mostfreq = np.where(np.max(frequencies) == frequencies)[0]
            if len(mostfreq) > 1:
                print("Warning: Frequency of shot length is equally distributed. No clear maximum. Decision criteria can't be used.")
                mostfreq=mostfreq[0]
            else:
                desired_lower = bins[mostfreq[0]]
                desired_upper = bins[mostfreq[0]+1]  
                print("Mean shot duration: "+str(shotMean/1E6)+" +- "+str(shotDev/1E6))
                print("Most frequent shot duration between "+str(desired_lower/1E6)+" and "+str(desired_upper/1E6)+" ms.")                                                                                                                  
                
            print(str(len(self.shots))+' shots detected.')
            print(str(len(self.errPosEdges))+' positive edges left.')
            print(str(len(self.errNegEdges))+' negative edges left.')            
                                                    
            return self.shots           
                                
        if searchMode == 'match':
            if (not 'file' in kwargs.keys())&(not 'list' in kwargs.keys()):
                raise ValueError("for search mode 'match', you have to provide a file containing timestamps or a list with timestamps")
            
            if 'file' in kwargs.keys():
                # detect all shots in timestamp range given by file            
                self.searchShots(searchin=[searchin['name']], file=kwargs['file'])
            if 'list' in kwargs.keys():
                if kwargs['list'] is list:
                    tsStart = np.min(kwargs['list'])
                    tsStop = np.max(kwargs['list'])
                    self.searchShots(searchin=[searchin['name']],start=tsStart,stop=tsStop)
                else:
                    raise ValueError("expected datatype 'list' for input argument keyword 'list'")
                
            if len(self.shots) > 0:
                                                   
                print("Matching detected shots with timestamps...")
                invalidTs = []
                matchedShots = []             
                #init progressbar
                if self.progressbar:
                    bar = progressBar(total=len(resPosEdgesTs))
                    counter = 0
                    
                # then assign each shot to a timestamp in the file
                for ts in self.timestamps['numeric']:
                    #determine all shots which begin on or after timestamp
                    begins = np.array([shot['begin'] for shot in self.shots])

                    relevant = np.where(begins >= (ts - ttol))[0]

                    if relevant.size == 0:
                        invalidTs.append(ts)
                        continue
                            
                    distances = [i - ts for i in begins[relevant]]
                    min_distance = np.min(np.abs(distances))
                    min_distance_index = np.where(np.abs(distances) == min_distance)                              
                    
                    if min_distance <= ttol:
                        foo=self.shots[relevant[min_distance_index]]
                        foo.update({'matchedTimestamp':ts,'auxTimestampInfo':self.timestamps['aux'][self.timestamps['numeric'].index(ts)]})
                        self.matchedShots.append(foo)
                    else:
                        invalidTs.append(ts)
                                   
                    if self.progressbar:
                        counter += 1                                                    
                        bar.update(counter)                                     
                    
                if self.progressBar:
                    bar.finish()
                    
                print(str(len(self.matchedShots))+' shots matched.')
                                                            