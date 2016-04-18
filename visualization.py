# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:48:45 2016

@author: Ned
"""
from __future__ import division
from pylab import *
import matplotlib.pyplot as plt
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
def heatmap(locations, pLocations,xSize,ySize,xl,yl,plot_title):
    errorMap = np.zeros((xSize,ySize))
    locDifferences = []
    xyz = zip(*locations)
    xmin = map(min,xyz)[0]
    ymin = map(min,xyz)[1]
    xmax = map(max,xyz)[0]
    ymax = map(max,xyz)[1]
    for l in range(len(locations)):
        locDifferences.append([pLocations[l][0]-locations[l][0],
                               pLocations[l][1]-locations[l][1], pLocations[l][2]-locations[l][2]])
    
    i = 0
    for x in range(xSize):
        for y in range(ySize):
            errMagnitude = sqrt((locDifferences[i][0])**2 + (locDifferences[i][1])**2)
            errorMap[x,y] = errMagnitude
            i += 1

    y, x = np.meshgrid(yl,xl)    
    
    plt.pcolor(x,y,errorMap,cmap='bwr',vmin=0,vmax=0.75)
    plt.axis([0,10,0,10])
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title(plot_title)
    
    # plt.imshow(errorMap, cmap=cm.RdBu, vmax=abs(errorMap).max(), vmin=0,
    #            extent = [xmin,xmax,ymin,ymax],interpolation='bilinear')
    #im.set_interpolation('nearest')
    #im.set_interpolation('bicubic')
    #im.set_interpolation('bilinear')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel("Position Error (m)")

    #ax.set_image_extent(-3, 3, -3, 3)

    plt.show()
    return errorMap
    rangesToUseInLocalization = get_simple_ranges('staticTagLong.txt')


def heat_weights(locations, weights, xSize, ySize, xl, yl):
    weightsMap = np.zeros((xSize,ySize))
    i = 0
    for x in range(xSize):
        for y in range(ySize):
            weightsMap[x,y] = weights[i]
            i += 1
    y,x = np.meshgrid(yl,xl)

    plt.pcolor(x,y,weightsMap,cmap='RdBu',vmin=0,vmax=1)
    plt.axis([0,10,0,10])
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title("Estimator Weights Based on RSSI")
    
    # plt.imshow(errorMap, cmap=cm.RdBu, vmax=abs(errorMap).max(), vmin=0,
    #            extent = [xmin,xmax,ymin,ymax],interpolation='bilinear')
    #im.set_interpolation('nearest')
    #im.set_interpolation('bicubic')
    #im.set_interpolation('bilinear')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel("Weight Value")

    #ax.set_image_extent(-3, 3, -3, 3)

    plt.show()





#when running this file alone, test the heatmap function
if __name__ == "__main__":
    # execute only if run as a script
    absLocations, estLocations = fakeLocations()
    a = heatmap(absLocations,estLocations,100,100)
    
