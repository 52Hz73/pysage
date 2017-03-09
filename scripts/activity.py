from lib.core import ShotHandler,ShotData
from lib.analysis import activity
from lib.aux import progressBar
import matplotlib.pyplot as plt
import numpy as np
import sys,os,time

print("------------------------------------------")
print("|Activity Analysis for Gyrotron Shot Data|")
print("------------------------------------------")
print("(c) 2016 Fabian Wilde, IPP-HGW")

start=time.time()

if len(sys.argv) < 2:
    raise ValueError('Error: expecting command line argument for input path(s) and output path (last path).')

am = activity()

for i in range(1,len(sys.argv)-1,1):
    mypath = sys.argv[i]
    files = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        files.extend(filenames)
        break
    
    print("Read directory "+mypath+"...")
    
    counter = 0
    start2=time.time()
    for filename in files:           
        #try:
        am.addData(src=mypath+filename,avgt=-10.0E-3)                        
        #except Exception as e:
        #    print("")
        #    print("Error:"+str(e))
        #    print("File skipped. Continue with next file.")
        #    continue
        print("")
        print("Directory progress:"+str(np.round((float(counter)/float(len(files)))*100.0,2))+"  %")
    
        counter+=1
    stop2=time.time()
    print("")
    print("Time elapsed:"+str((stop2-start2))+" seconds")
    print("Total progress:"+str(np.round((float(i)/float(len(sys.argv)-2))*100.0,2))+"  %")
    print("") 

print("Saving result of data reduction...")
am.saveData(dest=sys.argv[-1]) 

print("Total no. of shots evaluated:"+str(len(am.U['avg'])))

#print("Plot activity map...")
#am.plotActivityMap(save="output/activitymap_Bravo5.png")

stop=time.time()
print("")
print("Finished.")
print("Total time elapsed: "+str((stop-start))+" seconds")
