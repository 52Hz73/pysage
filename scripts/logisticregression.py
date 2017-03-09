from lib.analysis import activity
from matplotlib import pyplot as plt
import numpy as np

foo=activity()
foo.load(src="output/activityMap_Bravo5.npy")

bin_variable = []
U = []
I = []
Activity = []
#create dataset for binary logistic regression
for duration in foo.Durations:
    if (duration/1E6) < 999:
        bin_variable.append(0)
    else:
        bin_variable.append(1)
    U.append(foo.UResult['avg'])
    I.append(foo.IResult['avg'])
    Activity.append(foo.ActivityResult['avg'])
        
