# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 11:05:19 2015

@author: nedshelt
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tkFileDialog
from scipy import stats
from mayavi import mlab
import DWFunctions as dw


sns.set(style="ticks")

DisplayAnything3D = True
DisplayPath = False
DisplayContour = True
DisplayPoints = True
Display2DHistogram = True
DisplayAnchors = False  #May make 3D plots of static data too small to see
ZeroAboutFirstPoint = False
FileSelectDialog = True
PrintRanges = True
PointsOnHistogram = True




#Open the Decawave log file recorded by DecaRange RTLS
if FileSelectDialog:
    filepath = tkFileDialog.askopenfilename(filetypes=[("Text files","*.txt")])
else:
    filepath = "log.txt"
f = open(filepath)



trail = [] #a trail of crumbs, or list of all recorded locations
anchors = [] #an anchor is one of ths static radio positions
#step through and parse the log
for line in f:
    if ("LE" in line) and ("nan" not in line): #LE lines contain Location Estimates
        newCrumb = dw.Crumb(line)
        trail.append(newCrumb)
    if ("AP:0" in line) or ("AP:1" in line) or ("AP:2" in line):
        newAnchor = dw.Anchor(line)
        anchors.append(newAnchor)
        


# the x,y,and z values for the map and anchors
x = []
y = []
z = []

Ax = []
Ay = []
Az = []

for anc in anchors:
    Ax.append(anc.x)
    Ay.append(anc.y)
    Az.append(anc.z)

for crumbs in trail:
    x.append(crumbs.x)
    y.append(crumbs.y)
    z.append(crumbs.z)
    
x = np.array(x) #convert to numpy arrays for griddata
y = np.array(y)
z = np.array(z)

Ax = np.array(Ax) #convert to numpy arrays for anchor griddata
Ay = np.array(Ay)
Az = np.array(Az)

if ZeroAboutFirstPoint:
    x0 = x[0]
    y0 = y[0]
    z0 = z[0]
    
    x = x-x0
    y = y-y0
    z = z-z0
    Ax = Ax-x0
    Ay = Ay-y0
    Az = Az-z0


max_hyp = np.sqrt(max([x[i]**2 + y[i]**2 for i in range(len(x))]))
xmin = min(x)
xmax = max(x)
ymin = min(y)
ymax = max(y)
zmin = min(z)
zmax = max(z)
if PrintRanges:
    print "X Range:%s m" % (xmax-xmin)
    print "Y Range:%s m" % (ymax-ymin)
    print "Z Range:%s m" % (zmax-zmin)
    print "Max Err:%s m" % (max_hyp)

if (((xmax-xmin)+(ymax-ymin))/2) > 1:
    PointScale = .02
else:
    PointScale = .002
#==========ISO Surface=========
data = np.column_stack((x,y,z))
values = data.T

kde = stats.gaussian_kde(values)

# Create a regular 3D grid with 50 points in each dimension
xmin, ymin, zmin = data.min(axis=0)
xmax, ymax, zmax = data.max(axis=0)
xi, yi, zi = np.mgrid[xmin:xmax:50j, ymin:ymax:50j, zmin:zmax:50j]

# Evaluate the KDE on a regular grid...
coords = np.vstack([item.ravel() for item in [xi, yi, zi]])
density = kde(coords).reshape(xi.shape)

# Visualize the density estimate as isosurfaces
if DisplayAnything3D:
    if DisplayContour:
        mlab.contour3d(xi, yi, zi, density, opacity=0.5)
    if DisplayPath:
        mlab.plot3d(x,y,z)
    if DisplayPoints:
        mlab.points3d(x,y,z,scale_factor=PointScale)
    if DisplayAnchors:
        mlab.points3d(Ax,Ay,Az,scale_factor = 2*PointScale, color = (.9,0.,0.))
    mlab.axes()
    mlab.show()

#==========End ISO Surface=========


#=================2D Histogram=====
xAvg = "%.3f" % x.mean()
yAvg = "%.3f" % y.mean()
zAvg = "%.3f" % z.mean()

if Display2DHistogram:
    histogram = sns.jointplot(x, y, kind="kde",size=8,color="Green",stat_func=None);#kde / hex
    if PointsOnHistogram:
        histogram.plot_joint(plt.scatter, alpha=.2)
plt.title('DW X-Y Distribution({},{},{})'.format(xAvg,yAvg,zAvg))


    
    
f.close #remember to close the file after reading
