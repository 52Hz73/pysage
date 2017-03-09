# Gyrotron Shot Data Backup Script
#
# The script uses the PySAGE framework, Python 3.x, NumPy and SciPy.
#
# Description:
# This script is used to download shot data from the webarchive and save it as numpy files.
# It expects either an interval defined by two timestamps or a timestamp file.
# Then the script either searches for shots in the time interval using the data channel defined as the search channel.
# Either the script yields all shots it can find within the specified time range (mode 'allinrange') or it yields only
# the shots matching the timestamps in the given input file (mode 'match').
#
# Author:
# Fabian Wilde, IPP-HGW
# Date:
# December 2016

from lib.core import ShotHandler, ShotData
from lib.aux import progressBar
import matplotlib.pyplot as plt
import numpy as np
import sys, os, time

print("----------------------------------")
print("|Gyrotron Shot Data Backup Script|")
print("----------------------------------")
print("(c) 2016 Fabian Wilde, IPP-HGW")

# define shot data configuration here
sc = ShotData()

if sys.argv[4] == "A5":
	sc.addChannel(name='UBody', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/1/UB_A5/scaled/')
	sc.addChannel(name='RF', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/0/Rf_A5/scaled/')
	sc.addChannel(name='UCathode', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/3/UC_A5/scaled/')
	sc.addChannel(name='Activity', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/13/IGip_B5/unscaled/')
	sc.addChannel(name='ICathode', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/4/IC_A5/scaled/')
	# self.addChannel(name='SA',url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/1/UB_A5/unscaled/')
	sc.addChannel(name='SA', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/5/IGip_A5/unscaled/')
	sc.addChannel(name='Imain', url='codac/W7X/CoDaStationDesc.69/DataModuleDesc.148_DATASTREAM/3/A5_I_main/')
	sc.addChannel(name='Igun', url='codac/W7X/CoDaStationDesc.69/DataModuleDesc.148_DATASTREAM/4/A5_I_gun/')
	# sc.addChannel(name='Igp1', url='codac/W7X/CoDaStationDesc.72/DataModuleDesc.154_DATASTREAM/44/I_IGP1/')
	# sc.addChannel(name='Igp2', url='codac/W7X/CoDaStationDesc.72/DataModuleDesc.154_DATASTREAM/45/I_IGP2/')
	# sc.addChannel(name='Igp4', url='codac/W7X/CoDaStationDesc.72/DataModuleDesc.154_DATASTREAM/46/I_IGP4/')

if sys.argv[4] == "B5":
	sc.addChannel(name='UBody', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/9/UB_B5/scaled/')
	sc.addChannel(name='RF', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/8/Rf_B5/scaled/')
	sc.addChannel(name='UCathode', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/11/UC_B5/scaled/')
	sc.addChannel(name='Activity', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/13/IGip_B5/unscaled/')
	sc.addChannel(name='ICathode', url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/12/IC_B5/scaled/')
	# sc.addChannel(name='SA',url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/1/UB_A5/unscaled/')
	# sc.addChannel(name='SA',url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/5/IGip_A5/unscaled/')
	# sc.addChannel(name="SA",url='codac/W7X/CoDaStationDesc.106/DataModuleDesc.237_DATASTREAM/14/Bolo_B5/unscaled/')
	sc.addChannel(name='Imain', url='codac/W7X/CoDaStationDesc.69/DataModuleDesc.146_DATASTREAM/3/B5_I_main/')
	sc.addChannel(name='Igun', url='codac/W7X/CoDaStationDesc.69/DataModuleDesc.146_DATASTREAM/4/B5_I_gun/')
	# sc.addChannel(name='Igp1',url='codac/W7X/CoDaStationDesc.72/DataModuleDesc.156_DATASTREAM/44/I_IGP1/')
	# sc.addChannel(name='Igp2',url='codac/W7X/CoDaStationDesc.72/DataModuleDesc.156_DATASTREAM/45/I_IGP2/')
	# sc.addChannel(name='Igp4',url='codac/W7X/CoDaStationDesc.72/DataModuleDesc.156_DATASTREAM/46/I_IGP4/')

start = time.time()

if len(sys.argv) < 5:
    raise ValueError('Error: expecting command line argument for input path, output path and mode (allinrange or match).')
mypath = sys.argv[1]
files = []
for (dirpath, dirnames, filenames) in os.walk(mypath):
    files.extend(filenames)
    break

# scan given input directory for input files
counter = 0
for filename in files:
    start2 = time.time()
    print("File progress:" + str(np.round((float(counter) / float(len(files))) * 100.0, 2)) + "  %")
    # here the shot data configuration is set
    sc.channels['UBody'].clear()
    foo = ShotHandler(config=sc)
    try:
        # search for shots using data from channel 'UBody'
        # It's the easiest thing to do, since UBody has sharp edges on both begin and end of each shot
        result = foo.searchShots(searchin='UBody', \
                             mode=sys.argv[3], file=mypath + filename)

    except Exception as e:
        print("")
        print("Error:" + str(e))
        print("File skipped. Continue with next file.")
        continue
    # then download the full data for each found shot
    foo.downloadShot(src="search")
    # then save the full raw shot data for all channels
    # the maximum number of shots per file has to be limited
    # NumPy files bigger than 2 GB can be written but they cannot be read anymore due to 32bit limitations in NumPy
    foo.saveShots(dest=sys.argv[2])
    counter += 1
    stop2 = time.time()
    print("")
    print("Time elapsed:" + str((stop2 - start2)) + " seconds")
    print("")

stop = time.time()
print("")
print("Total time elapsed: " + str((stop - start)) + " seconds")
