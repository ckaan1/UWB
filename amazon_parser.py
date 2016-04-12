# -*- coding: utf-8 -*-
"""
@author: nedshelt
"""



#Serial input parser
def parseLine(lineIn):
    outDict = {}
    values = lineIn.split(' ')
    outDict['anchor'] = int(values[0].strip('ma'))
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

#==============================================================================
# For testing  without live serial data
#==============================================================================

#takes a .txt log file name, returns a list of lists of matching anchor/distance tuples
# tuples are in the form (anchor #, distance in meters), and grouped into lists corresponding
#to one set of ranges suitable for localization - usually [(A1,D1),(A2,D2),(A3,D3),(A4,D4)]
def get_simple_ranges(filename = 'staticTagLong.txt'):
    f = open(filename)
    sequence = []  #empty array of parsed lines. used as a buffer while waiting for 
    #            enough data to generate a range estimate. (255 long circular buff).
    #            This is useful when reading in data in real time
    for i in range(256):
        sequence.append([])
    lastSeq = 0
    
    simpleDists = []
    for line in f:
        d = parseLine(line)
        thisSeq = d['rangeSeq']
        sequence[thisSeq].append(d)
        #print d
        if thisSeq != lastSeq:  #if we have moved on to a new sequence, calculate the last one
            dists = []
            for anc in sequence[lastSeq]:
                dists.append((anc['anchor'],anc['meters']))
            simpleDists.append(dists)
            lastSeq = thisSeq
            if thisSeq == 0: #when the seqNum overflows, clear the sequence buffer
                for i in range(0,256):
                    sequence[i] = []
    f.close()
    simpleDists.pop(0) #frequently there won't be enough anchor data in the first set, so just remove it
    return simpleDists


#==============================================================================
# Example usage
#==============================================================================
rangesToUseInLocalization = get_simple_ranges('staticTagLong.txt')


