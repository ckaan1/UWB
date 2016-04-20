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
	env = Environment(4)
	print "Boundaries\n", env.boundaries
	print "Obstacles\n", env.obstacles

	# Setup Anchor locations
	anchors = []
	anchors.append(AnchorNode(0.3048,0.3048,0,0.025))
	anchors.append(AnchorNode(0.3048,9.6952,0,0.025))
	anchors.append(AnchorNode(9.6952,0.3048,0,0.025))
	anchors.append(AnchorNode(9.6592,9.6592,0,0.025))
	#anchors.append(AnchorNode(2.5,4,0,0.025))

	# Initialize beacon with starting location
	beacon = BeaconNode(0.5,0.5,0)

	## Setup variables to be used to create a distribution of points across environment
	upper_x = env.boundaries['x'][1]
	lower_x = env.boundaries['x'][0]
	upper_y = env.boundaries['y'][1]
	lower_y = env.boundaries['y'][0]
	length = 200

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

				distance.append(get_distance(a,bp,collision))
		distances.append(distance)

	# errorMap = np.zeros((length,length))
	# i = 0
	# for x in range(length):
	# 	for y in range(length):
	# 		ap = anchors[3].get_pos()
	# 		if distances[i][3]==0:
	# 			errorMap[x,y] = 0
	# 		else:
	# 			errorMap[x,y] = abs( distances[i][3] - ((beacon_positions[i,0]-ap['x'])**2 + (beacon_positions[i,1]-ap['y'])**2)**0.5 )
	# 		i += 1

	# y, x = np.meshgrid(beacon_positions_y,beacon_positions_x)    
    
	# plt.pcolor(x,y,errorMap,cmap='RdBu',vmin=0,vmax=1)
	# plt.axis([0,10,0,10])
	# plt.xlabel("X position (m)")
	# plt.ylabel("Y position (m)")
	# plt.title("Distance Error (m)")
	# plt.colorbar()

	# plt.show()

	# Use position solver on the estimated distances
	weighted_estimated_pos = np.zeros((len(beacon_positions),3))
	unweighted_estimated_pos = np.zeros((len(beacon_positions),3))
	# Use middle of room for guess
	x_guess = np.array([5,5])

	all_weights = np.zeros((len(distances),len(anchors)))
	for i in range(len(distances)):

		a_pos = np.zeros((len(anchors),2))
		for j in range(len(anchors)):
			pos = anchors[j].get_pos()
			a_pos[j] = [pos['x'],pos['y']]

		d = distances[i]
		a_d = np.array(d)

		if sum(d)==0:
			weighted_estimated_pos[i] = beacon_positions[i]
		else:
			## Use a solver to provide estimated position
			## NLLS solver
			weights = []
			for j in range(0,len(anchors)):
				expected_rssi = get_expected_rssi(a_d[j,0])
				weights.append(max( min( 1,(1-(abs(a_d[j,1]-expected_rssi)/5)) ), 0.1 ))
			all_weights[i,:] = weights
			p_estimate = NLLS_opt(x_guess,a_pos,a_d[:,0],weights)
			## ML solver
			# p_estimate = ML_opt(x_guess,a_pos,a_d)
			weighted_estimated_pos[i] = [p_estimate[0],p_estimate[1],0]

	for i in range(len(distances)):

		a_pos = np.zeros((len(anchors),2))
		for j in range(len(anchors)):
			pos = anchors[j].get_pos()
			a_pos[j] = [pos['x'],pos['y']]

		d = distances[i]
		a_d = np.array(d)

		if sum(d)==0:
			unweighted_estimated_pos[i] = beacon_positions[i]
		else:
			## Use a solver to provide estimated position
			## NLLS solver
			weights = []
			for j in range(0,len(anchors)):
				weights.append(1)
			p_estimate = NLLS_opt(x_guess,a_pos,a_d[:,0],weights)
			## ML solver
			# p_estimate = ML_opt(x_guess,a_pos,a_d)
			unweighted_estimated_pos[i] = [p_estimate[0],p_estimate[1],0]


	plt.figure(1)
	for i in range(len(anchors)):
		ap = anchors[i].get_pos()
		fig = plt.figure(1)
		ax1 = fig.add_subplot(111,aspect='equal')
		p = ptc.Circle((ap['x'],ap['y']),radius=0.2,edgecolor="#ff8000",facecolor='#ff8000')
		ax1.add_patch(p)
	env.draw_obstacles(1)
	heatmap(beacon_positions,weighted_estimated_pos,length,length,beacon_positions_x,beacon_positions_y,'Simulated Weighted Least Squares Estimator')

	plt.figure(2)
	env.draw_obstacles(2)
	for i in range(len(anchors)):
		ap = anchors[i].get_pos()
		fig = plt.figure(2)
		ax1 = fig.add_subplot(111,aspect='equal')
		p = ptc.Circle((ap['x'],ap['y']),radius=0.2,edgecolor="#ff8000",facecolor='#ff8000')
		ax1.add_patch(p)
	heatmap(beacon_positions,unweighted_estimated_pos,length,length,beacon_positions_x,beacon_positions_y,'Simulated Unweighted Least Squares Estimator')

	for i in range(3,len(anchors)+3):
		plt.figure(i)
		env.draw_obstacles(i)
		ap = anchors[i-3].get_pos()
		fig = plt.figure(i)
		ax1 = fig.add_subplot(111,aspect='equal')
		p = ptc.Circle((ap['x'],ap['y']),radius=0.2,edgecolor="#ff8000",facecolor='#ff8000')
		ax1.add_patch(p)
		heat_weights(beacon_positions,all_weights[:,i-3],length,length,beacon_positions_x,beacon_positions_y)

	## Create a path to "follow"
	waypoints = [[2,2,0],[2.5,2,0],[2.5,5,0],[3,5,0],[3,7,0],[9,7,0],[9,1,0],[6.5,1,0],[6.5,1.5,0]]
	path_points = []

	step = .05
	j = 0
	path_points.append(waypoints[0])
	for i in range(0,len(waypoints)-1):
		while (path_points[j][0]!=waypoints[i+1][0]) or (path_points[j][1]!=waypoints[i+1][1]):
			new_x = 0
			new_y = 0
			if( abs(waypoints[i+1][0]-path_points[j][0])>step ):
				if( path_points[j][0]>waypoints[i+1][0] ):
					new_x = path_points[j][0]-step
				else:
					new_x = path_points[j][0]+step
			else:
				new_x = waypoints[i+1][0]
			if( abs(waypoints[i+1][1]-path_points[j][1])>step ):
				if( path_points[j][1]>waypoints[i+1][1] ):
					new_y = path_points[j][1]-step
				else:
					new_y = path_points[j][1]+step
			else:
				new_y = waypoints[i+1][1]
			path_points.append([new_x,new_y,0])
			j = j + 1

	path_distances = []
	# For each beacon position run the algorithm to obtain an estimated position
	for b_pos in path_points:
		path_distance = []
		# If the point is in an obstacle, return zeros
		if env.in_obstacle(b_pos):
			for a in anchors:
				path_distance.append(0)
		else:
			beacon.move_pos(b_pos[0],b_pos[1],b_pos[2])
			bp = beacon.get_pos()
			for a in anchors:
				ap = a.get_pos()
				collision = env.determine_NLOS([ap['x'],ap['y']],[bp['x'],bp['y']])

				path_distance.append(get_distance(a,bp,collision))
		path_distances.append(path_distance)

	print len(path_points)

	weighted_estimated_pos = np.zeros((len(path_points),3))
	unweighted_estimated_pos = np.zeros((len(path_points),3))
	# Use middle of room for guess
	x_guess = np.array([5,5])

	all_weights = np.zeros((len(path_distances),len(anchors)))
	for i in range(len(path_distances)):

		a_pos = np.zeros((len(anchors),2))
		for j in range(len(anchors)):
			pos = anchors[j].get_pos()
			a_pos[j] = [pos['x'],pos['y']]

		d = path_distances[i]
		a_d = np.array(d)

		if sum(d)==0:
			weighted_estimated_pos[i] = path_points[i]
		else:
			## Use a solver to provide estimated position
			## NLLS solver
			weights = []
			for j in range(0,len(anchors)):
				expected_rssi = get_expected_rssi(a_d[j,0])
				weights.append(max( min( 1,(1-(abs(a_d[j,1]-expected_rssi)/5)) ), 0.1 ))
			all_weights[i,:] = weights
			p_estimate = NLLS_opt(x_guess,a_pos,a_d[:,0],weights)
			## ML solver
			# p_estimate = ML_opt(x_guess,a_pos,a_d)
			weighted_estimated_pos[i] = [p_estimate[0],p_estimate[1],0]

	for i in range(len(path_distances)):

		a_pos = np.zeros((len(anchors),2))
		for j in range(len(anchors)):
			pos = anchors[j].get_pos()
			a_pos[j] = [pos['x'],pos['y']]

		d = path_distances[i]
		a_d = np.array(d)

		if sum(d)==0:
			unweighted_estimated_pos[i] = path_points[i]
		else:
			## Use a solver to provide estimated position
			## NLLS solver
			weights = []
			for j in range(0,len(anchors)):
				weights.append(1)
			p_estimate = NLLS_opt(x_guess,a_pos,a_d[:,0],weights)
			## ML solver
			# p_estimate = ML_opt(x_guess,a_pos,a_d)
			unweighted_estimated_pos[i] = [p_estimate[0],p_estimate[1],0]


	plt.figure(1)
	for i in range(len(anchors)):
		ap = anchors[i].get_pos()
		fig = plt.figure(1)
		ax1 = fig.add_subplot(111,aspect='equal')
		p = ptc.Circle((ap['x'],ap['y']),radius=0.2,edgecolor="#ff8000",facecolor='#ff8000')
		ax1.add_patch(p)
	env.draw_obstacles(1)
	plt.xlabel("X position (m)")
	plt.ylabel("Y position (m)")
	plt.title("Actual Path versus Estimated Path with Weighting")
	scatter_path(np.array(path_points),weighted_estimated_pos)

	plt.figure(2)
	for i in range(len(anchors)):
		ap = anchors[i].get_pos()
		fig = plt.figure(2)
		ax1 = fig.add_subplot(111,aspect='equal')
		p = ptc.Circle((ap['x'],ap['y']),radius=0.2,edgecolor="#ff8000",facecolor='#ff8000')
		ax1.add_patch(p)
	env.draw_obstacles(2)
	plt.xlabel("X position (m)")
	plt.ylabel("Y position (m)")
	plt.title("Actual Path versus Estimated Path without Weighting")
	scatter_path(np.array(path_points),unweighted_estimated_pos)

	raw_input("Press enter to exit...")
 


