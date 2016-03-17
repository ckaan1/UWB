# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 11:05:19 2015

@author: nedshelt
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks")

#Open the Decawave log file recorded by DecaRange RTLS
f = open("log.txt","r")

# A crumb is a single recorded position, with time and other data
class Crumb(object): 
    def __init__(self,input_string):#parses a Log string to crumb variables
        s = input_string.split(":")
        s[6] = s[6].replace("[","")
        s[6] = s[6].replace("]","")
        xyz = s[6].split(",")
        self.time = s[1]
        self.ID = int(s[3])
        self.LEcount = int(s[4])
        self.SequenceNum = int(s[5])
        self.x = float(xyz[0])
        self.y = float(xyz[1])
        self.z = float(xyz[2])
        self.A0 = float(s[7])
        self.A1 = float(s[8])
        self.A2 = float(s[9])
        self.A3 = float(s[10])
        
def printCrumb(inCrumb): #for debugging
    print "==============="
    print "%s (time)" % inCrumb.time
    print "%d (ID)" % inCrumb.ID
    print "%s (LE count)" % inCrumb.LEcount
    print "%d (Sequence number)" % inCrumb.SequenceNum
    print "%f (x)" % inCrumb.x
    print "%f (y)" % inCrumb.y
    print "%f (z)" % inCrumb.z
    print "%f (A0 dist)" % inCrumb.A0
    print "%f (A1 dist)" % inCrumb.A1
    print "%f (A2 dist)" % inCrumb.A2
    print "%f (A3 dist)" % inCrumb.A3
    print "==============="



trail = [] #a trail of crumbs, or list of all recorded locations

for line in f:
    if ("LE" in line) and ("nan" not in line): #LE lines contain positions
        newCrumb = Crumb(line)
        trail.append(newCrumb)

#printCrumb(newCrumb)

# the x,y,and z values for the map
x = []
y = []
z = []

for Crumb in trail:
    x.append(Crumb.x)
    y.append(Crumb.y)
    z.append(Crumb.z)
    
x = np.array(x) #convert to numpy arrays for griddata
y = np.array(y)
z = np.array(z)

#xmin = min(x)
#xmax = max(x)
#ymin = min(y)
#ymax = max(y)

sns.jointplot(x, y, kind="kde",size=8,color="Purple",stat_func=None);#dke or hex

plt.title('X-Y Distribution')

f.close #remember to close the file after reading
