# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:02:41 2015

@author: nedshelt
"""

import serial
import time
import localization as lx
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = []
y = []
z = []



P=lx.Project(mode='2D',solver='CCA')  #Setting up location solver
#P.add_anchor('a00',(12.355,54.791,2.87)) #for now, these are hardcoded because the anchors are
#P.add_anchor('a01',(18.146,65.261,2.87)) #fixed on the floor. A plaintext configuration file
#P.add_anchor('a02',(12.355,78.680,2.87)) #would work well to store an arbitrary # of anchors
#P.add_anchor('a03',(18.146,83.548,2.87))


#temporary for testing, matches what DW ranginer app sees.
P.add_anchor('a00',(0,0,2.87)) #for now, these are hardcoded because the anchors are
P.add_anchor('a01',(5.791,10.47,2.87)) #fixed on the floor. A plaintext configuration file
P.add_anchor('a02',(0,23.889,2.87)) #would work well to store an arbitrary # of anchors
P.add_anchor('a03',(5.791,28.757,2.87))

target,label=P.add_target()  #initialize the target to solve the position of


#def scan():
#   # scan for available ports. return a list of tuples (num, name)
#   available = []
#   for i in range(256):
#       try:
#           s = serial.Serial(i)
#           available.append( (i, s.portstr))
#           s.close()
#       except serial.SerialException:
#           pass
#   return available
#
#print "Found ports:"
#for n,s in scan(): print "(%d) %s" % (n,s)
#user_port = raw_input("Which port is the DecaWave board connected to?")
#ser = serial.Serial(user_port,115200)
#
#print(ser.readline())
#
#ser.close()


#Serial input parser
def parseLine(lineIn):
    outDict = {}
    values = lineIn.split(' ')
    outDict['anchor'] = values[0].strip('m')
    outDict['tag'] = int(values[1].strip('t'))
    outDict['meters'] = float(int(values[2], base=16))/1000
    outDict['rawmm'] = int(values[3], base=16)
    outDict['rangeNum'] = int(values[4], base=16)
    outDict['rangeSeq'] = int(values[5], base=16)  #this will be mod 256
    outDict['rangeTimems'] = int(values[6], base=16)
    outDict['board'] = int(values[9][1:2])  #board that this computer is connected to
    
    return outDict

def isNext(nextVal,thisVal):# the ranging sequence is mod 256, this checks if it is incrimented
    if (thisVal == 255 and nextVal == 0):
        return True
    else:
        return (nextVal > thisVal)

#pass the solver distances, solve for location, and return the results
def localize(rangeArray):
    if len(rangeArray) > 2:    
        print('=====')
        target.measures = []
        for measurement in rangeArray:
            #print measurement['meters']
            target.add_measure(measurement['anchor'],measurement['meters'])
        P.solve()
        print(target.loc.x,target.loc.y,target.loc.z)
        x.append(target.loc.x)  #these variables are being used for testing
        y.append(target.loc.y)
        z.append(target.loc.z)
    else:
        print "Not enough anchors to localize ({})".format(len(rangeArray))



#==============================================================================
# For testing  without live serial data
#==============================================================================
f = open('cinderblock.txt')
sequence = []  #empty array of parsed lines. used as a buffer while waiting for 
#            enough data to generate a range estimate. (255 long circular buff)
for i in range(256):
    sequence.append([])
lastSeq = 0


for line in f:
    d = parseLine(line)
    thisSeq = d['rangeSeq']
    sequence[thisSeq].append(d)
    #print d
    if thisSeq != lastSeq:  #if we have moved on to a new sequence, calculate the last one
        localize(sequence[lastSeq])
        lastSeq = thisSeq
        if thisSeq == 0: #when the seqNum overflows, clear the sequence buffer
            for i in range(1,256):
                sequence[i] = []




x = np.array(x) #convert to numpy arrays for griddata
y = np.array(y)
z = np.array(z)
#x = x-x[0]
#y = y-y[0]
#z = z-z[0]
histogram = sns.jointplot(x,y,kind='kde',size=8,color='Purple',stat_func=None)

xAvg = "%.3f" % x.mean()
yAvg = "%.3f" % y.mean()
zAvg = "%.3f" % z.mean()


histogram.plot_joint(plt.scatter,alpha=.2)
plt.title('{} {} X-Y Distribution({},{},{})'.format(P.mode,P.solver,xAvg,yAvg,zAvg))


f.close()

