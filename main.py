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
	anchors.append(AnchorNode(5,0,0,0.05))
	anchors.append(AnchorNode(0,8,0,0.05))
	anchors.append(AnchorNode(5,8,0,0.05))
	anchors.append(AnchorNode(2.5,4,0,0.05))

	# Initialize beacon with starting location
	beacon = BeaconNode(0.5,0.5,0)

	## Setup variables to be used to create a distribution of points across environment
	upper_x = env.boundaries['x'][1]-0.1
	lower_x = env.boundaries['x'][0]+0.1
	upper_y = env.boundaries['y'][1]-0.1
	lower_y = env.boundaries['y'][0]+0.1
	length = 20

	# Build linspace for x and y positions
	beacon_positions_x = np.linspace(lower_x,upper_x,length)
	beacon_positions_y = np.linspace(lower_y,upper_y,length)
	# Setup array to hold all combinations of positions
	beacon_positions = np.zeros((length**2,3))
	for i in range(len(beacon_positions)):
		pos = [beacon_positions_x[i-length*(i/length)],beacon_positions_y[i/length],0]
		# Make sure the point created isn't inside an obstacle
		if env.in_obstacle(pos):
			continue
		else:
			beacon_positions[i] = pos
	# From all positions, any that were inside obstacles need to be pruned
	actual_positions = beacon_positions[~np.all(beacon_positions==0,axis=1)]

	error = []
	# For each actual position run the algorithm to obtain an estimated position
	for b_pos in actual_positions:
		# move beacon between tests
		beacon.move_pos(b_pos[0],b_pos[1],b_pos[2])
		distances = []
		bp = beacon.get_pos()
		print 'Beacon pos: ', bp
		for a in anchors:
			ap = a.get_pos()
			collision = env.determine_NLOS([ap['x'],ap['y']],[bp['x'],bp['y']])

			distances.append(get_distance(a,bp,collision,env.dielectric))

		error.append( abs( distances[3]-(((b_pos[0]-ap['x'])**2+(b_pos[1]-ap['y'])**2)**0.5) ) )
		print 'Distance Measurements for each anchor: ', distances
		
	#print actual_positions

	x, y = np.meshgrid(actual_positions[:,0],actual_positions[:,1])
	#print y
	#print x

	aerror = np.array(error)
	print aerror

	# generate 2 2d grids for the x & y bounds
	# y, x = np.mgrid[slice(-3, 3 + dy, dy),
 #                slice(-3, 3 + dx, dx)]
	# print y
	# print x

	plt.pcolor(x, y, aerror, cmap='RdBu', vmin=0, vmax=aerror.max())
	plt.title('pcolor')
	# set the limits of the plot to the limits of the data
	plt.axis([actual_positions[:,0].min(), actual_positions[:,0].max(), actual_positions[:,1].min(), actual_positions[:,1].max()])
	plt.colorbar()
	plt.show()

	## Test position solver using Non-Linear Least Square algorithm
	## Assume there are three fixed anchors
	x_guess = numpy.array([3, 3])  # a position guess for mobile tag
	p_FA = numpy.array([[0,0],[5,0],[2,5]])
	d_M = numpy.array([[2,2],[-3,2],[0,-3]])
	ps = Position_solver(x_guess,p_FA,d_M)
	x_estimate = ps.NLLS
	print "Estimate position of test1 using NLLS algorithm\n",x_estimate
	
	raw_input("Press enter to exit...")

