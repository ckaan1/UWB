import time
import sys
from anchor_nodes import *
from beacon_node import *
from environment import *
from experiments import *
from amazon_parser import get_simple_ranges
from localization_algorithms import *
from nlos_detection import *
from sensor_simulation import *
from position_solver import *
from visualization import *

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Setup Environment and display boundaries and obstacles
    env = Environment(3)
    print "Boundaries\n", env.boundaries
    print "Obstacles\n", env.obstacles

    # Setup Anchor locations
    anchors = []
    anchors.append(AnchorNode(.27305,.8763,0,0.025))
    anchors.append(AnchorNode(5.70865,0.76835,0,0.025))
    anchors.append(AnchorNode(5.6769,6.3373,0,0.025))
    anchors.append(AnchorNode(.288036,6.59638,0,0.025))

    # Initialize beacon with starting location
    beacon = BeaconNode(2.94435,3.53445,0)

    



    realRanges = get_simple_ranges('walkingIntermittentNLOS.txt')
    
    
    
     # Use position solver on the estimated distances
    # estimated_pos = np.zeros((len(beacon_positions),3))
     # Use middle of room for guess
    x_guess = np.array([2.5,4])
    estimated_pos = []
    for i in range(len(realRanges)):
        if len(realRanges[i])==4: #only if we have data from all 4 anchors
            a_pos = np.zeros((len(anchors),2))
            for j in range(len(anchors)):
                pos = anchors[j].get_pos()
                a_pos[j] = [pos['x'],pos['y']]

            d = realRanges[i]
            a_d = np.array(d)


             ## Use a solver to provide estimated position
             ## NLLS solver
            p_estimate = NLLS_opt(x_guess,a_pos,a_d)
             ## ML solver
             # p_estimate = ML_opt(x_guess,a_pos,a_d)
            #estimated_pos[i] = [p_estimate[0],p_estimate[1],0]
            estimated_pos.append([p_estimate[0],p_estimate[1],0])
    scatterX = []
    scatterY = []
    for p in estimated_pos:
        scatterX.append(p[0])
        scatterY.append(p[1])
    
    tagX = beacon.get_pos()['x']
    tagY = beacon.get_pos()['y']
    plt.scatter(scatterX,scatterY,c='r',marker='o')
    #plt.scatter(tagX,tagY,c='red')
    #heatmap(beacon_positions,estimated_pos,length,length,beacon_positions_x,beacon_positions_y)
    #plt.axis([1.5,5,2,5.5])
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title("LOS (blue) vs NLOS (red) Position Estimates")
    plt.axes().set_aspect('equal', 'datalim')

 


