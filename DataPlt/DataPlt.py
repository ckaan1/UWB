# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 16:31:23 2016
Histogram of Test Data in Outdoor and LOS Scenario

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
plt.title('Histogram of UWB Test Data (Outdoor, LOS, distance = 2 m)')

plt.axis([1.8, 2.4, 0, 500])
plt.grid(True)
plt.show()

data_2 = data_import[2636:5224][1]
# the histogram of the data_1 (distance = 4 m)
plt.figure()
data_2.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (Outdoor, LOS, distance = 4 m)')

plt.axis([3.9, 4.4, 0, 400])
plt.grid(True)
plt.show()

data_3 = data_import[5484:8923][1]
# the histogram of the data_1 (distance = 8 m)
plt.figure()
data_3.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (Outdoor, LOS, distance = 8 m)')

plt.axis([8.0, 8.7, 0, 400])
plt.grid(True)
plt.show()

data_4 = data_import[9130:12000][1]
# the histogram of the data_1 (distance = 12 m)
plt.figure()
data_4.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (Outdoor, LOS,  distance = 12 m)')

plt.axis([12.0,12.6, 0, 200])
plt.grid(True)
plt.show()

data_5 = data_import[12766:14348][1]
# the histogram of the data_1 (distance = 8 m)
plt.figure()
data_5.hist(bins=100)


plt.xlabel('Distance (m)')
plt.ylabel('Distribution')
plt.title('Histogram of UWB Test Data (Outdoor, LOS, distance = 14 m)')

plt.axis([14.0, 14.7, 0, 250])
plt.grid(True)
plt.show()

# mean and standard deviation
m_1 = np.mean(data_1)
std_1 = np.std(data_1)
m_2 = np.mean(data_2)
std_2 = np.std(data_2)
m_3 = np.mean(data_3)
std_3 = np.std(data_3)
m_4 = np.mean(data_4)
std_4 = np.std(data_4)
m_5 = np.mean(data_5)
std_5 = np.std(data_5)

mean = [m_1, m_2,m_3,m_4,m_5]
Std = [std_1,std_2,std_3,std_4,std_5]
width = 0.35
mean_series = pd.Series.from_array(mean)  
Std_series = pd.Series.from_array(Std)  
x_labels = ['2 m', '4 m', '8 m', '12 m', '14 m']
# Mean
plt.figure()
ax = mean_series.plot(kind='bar')
ax.set_title("Mean of Test Data (LOS, Outdoor)")
ax.set_xlabel("Distance")
ax.set_ylabel("Mean")
ax.set_xticklabels(x_labels)

rects = ax.patches

# Now make some labels
labels = mean

for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height, label, ha='center', va='bottom')

# STD
plt.figure()
ax = Std_series.plot(kind='bar')
ax.set_title("STD of Test Data (LOS, Outdoor)")
ax.set_xlabel("Distance")
ax.set_ylabel("STD")
ax.set_ylim(0,0.09)
ax.set_xticklabels(x_labels)

rects = ax.patches

# Now make some labels
labels = Std
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height, label, ha='center', va='bottom')
