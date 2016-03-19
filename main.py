import time
import sys
from anchor_nodes import *
from beacon_node import *
from environment import *
from experiments import *
from localization_algorithms import *
from nlos_detection import *
from sensor_simulation import *
from position_solver import *
from visualization import *

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

	# Setup Environment and display boundaries and obstacles
	dielectric_constant = 1.55
	env = Environment(1,dielectric_constant)
	print "Boundaries\n", env.boundaries
	print "Obstacles\n", env.obstacles

	# Setup Anchor locations
	anchors = []
	anchors.append(AnchorNode(0,0,0,0.05))
	#anchors.append(AnchorNode(5,0,0,0.05))
	anchors.append(AnchorNode(0,8,0,0.05))
	#anchors.append(AnchorNode(5,8,0,0.05))
	anchors.append(AnchorNode(2.5,4,0,0.05))

	# Initialize beacon with starting location
	beacon = BeaconNode(0.5,0.5,0)

	## Setup variables to be used to create a distribution of points across environment
	upper_x = env.boundaries['x'][1]
	lower_x = env.boundaries['x'][0]
	upper_y = env.boundaries['y'][1]
	lower_y = env.boundaries['y'][0]
	length = 100

	# Build linspace for x and y positions
	beacon_positions_x = np.linspace(lower_x,upper_x,length)
	beacon_positions_y = np.linspace(lower_y,upper_y,length)
	# Setup array to hold all combinations of positions
	beacon_positions = np.zeros((length**2,3))
	for i in range(len(beacon_positions)):
		pos = [beacon_positions_x[(i/length)],beacon_positions_y[i-length*(i/length)],0]
		beacon_positions[i] = pos

	distances = []
	# For each beacon position run the algorithm to obtain an estimated position
	for b_pos in beacon_positions:
		distance = []
		# If the point is in an obstacle, return zeros
		if env.in_obstacle(b_pos):
			for a in anchors:
				distance.append(0)
		else:
			beacon.move_pos(b_pos[0],b_pos[1],b_pos[2])
			bp = beacon.get_pos()
			for a in anchors:
				ap = a.get_pos()
				collision = env.determine_NLOS([ap['x'],ap['y']],[bp['x'],bp['y']])

				distance.append(get_distance(a,bp,collision,env.dielectric))
		distances.append(distance)

	## Test position solver using Non-Linear Least Square algorithm
	estimated_pos = np.zeros((len(beacon_positions),3))
	for i in range(len(distances)):
		# Use middle of room for guess
		x_guess = np.array([2.5,4])

		a_pos = np.zeros((len(anchors),2))
		for j in range(len(anchors)):
			pos = anchors[j].get_pos()
			a_pos[j] = [pos['x'],pos['y']]

		d = distances[i]
		a_d = np.array(d)

		if sum(d)==0:
			estimated_pos[i] = beacon_positions[i]
		else:
			ps = Position_solver(x_guess,a_pos,a_d)
			p_estimate = ps.NLLS
			estimated_pos[i] = [p_estimate[0],p_estimate[1],0]

	heatmap(list(beacon_positions),list(estimated_pos),length,length,beacon_positions_y,beacon_positions_x)
	
	raw_input("Press enter to exit...")

