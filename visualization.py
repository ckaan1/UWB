# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:48:45 2016

@author: Ned
"""
from __future__ import division
from pylab import *
import numpy as np

#tool for generating sample exact position data, and estimated position data, with errors
def fakeLocations(xSize=5,ySize=5,stepSize = .05):
    absLocations = []
    estLocations = []
    Ax = arange(0,xSize,stepSize)
    Ay = arange(0,ySize,stepSize)
    
    for x in Ax:
        for y in Ay:
            #create a list of x,y,z positions
            absLocations.append([x,y,random()])
            #create location estimates with simulated error
            error = (1- x/2 + x**5 + y**3)*exp(-x**2-y**2)
            estLocations.append([x+error,y+error,random()])
    
    
    return absLocations, estLocations


#takes in absolute and pseudo positions over a map, plots a heatmap of error at each location
#expects positions coming in to iterate over y first, then x, for a full grid
#returns nothing
def heatmap(locations, pLocations,xSize,ySize):
    errorMap = np.zeros((xSize,ySize))
    locDifferences = []
    for l in range(len(locations)):
        locDifferences.append([pLocations[l][0]-locations[l][0],
                               pLocations[l][1]-locations[l][1], pLocations[l][2]-locations[l][2]])
    
    i = 0
    for x in range(xSize):
        for y in range(ySize):
            errMagnitude = sqrt((locDifferences[i][0])**2 + (locDifferences[i][1])**2)
            errorMap[x,y] = errMagnitude
            i += 1
    
    ax = subplot(111)
    im = imshow(errorMap, cmap=cm.RdBu, vmax=abs(errorMap).max(), vmin=0)
    #im.set_interpolation('nearest')
    #im.set_interpolation('bicubic')
    im.set_interpolation('bilinear')
    #ax.set_image_extent(-3, 3, -3, 3)

    show()
    return errorMap





#when running this file alone, test the heatmap function
if __name__ == "__main__":
    # execute only if run as a script
    absLocations, estLocations = fakeLocations()
    a = heatmap(absLocations,estLocations,100,100)
    
