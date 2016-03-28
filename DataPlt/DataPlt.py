# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 16:31:23 2016

@author: Qizong
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_import = pd.read_csv('data.csv', sep=',',header=None)
data_1 = data_import[0:2615][1]
# the histogram of the data_1 (distance = 2 m)
plt.figure()
data_1.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (LOS - distance = 2 m)')

plt.axis([1.8, 2.4, 0, 500])
plt.grid(True)
plt.show()

data_2 = data_import[2636:5224][1]
# the histogram of the data_1 (distance = 4 m)
plt.figure()
data_2.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (LOS - distance = 4 m)')

plt.axis([3.9, 4.4, 0, 400])
plt.grid(True)
plt.show()

data_3 = data_import[5484:8923][1]
# the histogram of the data_1 (distance = 8 m)
plt.figure()
data_3.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (LOS - distance = 8 m)')

plt.axis([8.0, 8.7, 0, 400])
plt.grid(True)
plt.show()

data_4 = data_import[9130:12000][1]
# the histogram of the data_1 (distance = 12 m)
plt.figure()
data_4.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (LOS - distance = 12 m)')

plt.axis([12.0,12.6, 0, 200])
plt.grid(True)
plt.show()

data_5 = data_import[12766:14348][1]
# the histogram of the data_1 (distance = 8 m)
plt.figure()
data_5.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (LOS - distance = 14 m)')

plt.axis([14.0, 14.7, 0, 250])
plt.grid(True)
plt.show()