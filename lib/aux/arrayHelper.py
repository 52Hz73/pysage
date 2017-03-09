import os, sys, time
import numpy as np

"""
Description:
class progressbar provides a customizable progress indicator

Author:
Fabian Wilde, IPP HGW

Date:
September 2016
"""

class arrayHelper(object):
    def getUniformAreas(self, arr, stol):
        d = np.diff(arr)
        test = np.where(d > stol)[0]
                        
        if test.size > 0:              
            foo = []
            old = 0                                   
            for elem in test:                  
                foo.append(arr[old:elem + 1])                   
                old = elem + 1
            foo.append(arr[old:])              
            return foo
        else:
            return [np.array(arr)]
        
    def getMiddleValue(self, arr):
        if len(arr) > 0:
            if len(arr) % 2 == 0:
                return arr[(len(arr) / 2) - 1]
            else:
                return arr[(len(arr) - 1) / 2]
        else:
            return None  

class progressBar(object):
    def __init__(self,**kwargs):
        if 'char' in kwargs.keys():
            self.char = kwargs['char']
        else:
            self.char = '#'
        if 'barlen' in kwargs.keys():
            if not type(kwargs['len']) is int:
                raise ValueError(" expecting integer for input argument 'len'.")
            self.barlen = kwargs['len']
        else:
            self.barlen = 50
        if 'bar' in kwargs.keys():
            if not kwargs['bar'] in [True,False]:
                raise ValueError(" expecting boolean or string representing boolean keyword for input argument 'bar'.")
            self.bar = kwargs['bar']
        else:
            self.bar = True
        if 'eta' in kwargs.keys():
            if not kwargs['eta'] in [True,False]:
                raise ValueError(" expecting boolean or string representing boolean keyword for input argument 'eta'.")
            self.eta = kwargs['eta']
        else:
            self.eta = True
        if 'spinner' in kwargs.keys():
            if not kwargs['spinner'] in [True,False]:
                raise ValueError(" expecting boolean or string representing boolean keyword for input argument 'spinner'.")
            self.spinner = kwargs['spinner']
        else:
            self.spinner = True
        if 'spinnerdat' in kwargs.keys():
            self.spinnerdat = kwargs['spinnerdat']
        else:
            self.spinnerdat = ['|','/','-','\\']
        if 'value' in kwargs.keys():
            if not type(kwargs['value']) is int:
                raise ValueError(" expecting integer for input argument 'value'.")
            self.value = kwargs['value']            
        else:
            self.value = 0
        if 'total' in kwargs.keys():
            if not type(kwargs['total']) is int:
                raise ValueError(" expecting integer for input argument 'total'.")
            self.total = kwargs['total']
        else:
            self.total = 100
        
        self.progress = round((float(self.value)/float(self.total))*100,2)
        self.timeLeft = -1
        self.times = []
        self.spinnerCount = 0
    
    def show(self):
        str2show = 'Progress: '+str(self.progress)+" % "
        if self.bar:
            #build progressbar
            numchars = int((self.progress/100)*self.barlen)
            str2show += "["
            #add bar characters according to progress value
            for i in range(0,numchars):
                str2show = str2show + self.char
            #fill up with white space
            if (self.barlen-numchars) > 0:
                for i in range(0,self.barlen-numchars):
                    str2show += " "
            str2show += "]"                     
            
        if self.eta:
            if self.timeLeft == -1:
                str2show += " - ETA: TBD"
            else:                
                hh = int(self.timeLeft / 3600)
                mm = int((self.timeLeft - hh*3600)/60)
                ss = int((self.timeLeft - hh*3600 - mm*60))
                str2show += " - ETA: "+str(hh)+":"+str(mm)+":"+str(ss)
                
        if self.spinner:
            self.spinnerCount += 1
            if self.spinnerCount > (len(self.spinnerdat)-1):
                self.spinnerCount = 0
            str2show += " " + self.spinnerdat[self.spinnerCount] + " "
             
        print(str2show,end='\r')    
    
    def update(self,value):
        self.times.append(time.time())
        self.value = value
        if self.value > self.total:
            self.value = self.total
        if len(self.times) >= 2:
            self.timeLeft = (self.total-self.value)*np.mean(np.diff(self.times))
        else:
            self.timeLeft = -1
        self.progress = round((float(self.value)/float(self.total))*100,2)
        self.show()
        
    def finish(self):
        self.update(self.total)
        print("")
        
    def clear(self):
        self.times = []
        self.timeLeft = -1
        self.progress = 0
            