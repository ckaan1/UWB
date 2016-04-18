import numpy as np

def estimated_distance(ap,bp,obstacles,c):

	total_distance = ((ap['x']-bp['x'])**2+(ap['y']-bp['y'])**2)**0.5
	d_plus = 0
	for o in obstacles:
		if obstacles[o]:
			for i in range(0,len(obstacles[o])-2):
				obstacle_distance = ((obstacles[o][1][0]-obstacles[o][0][0])**2+(obstacles[o][1][1]-obstacles[o][0][1])**2)**0.5
				dc = obstacles[o][len(obstacles[o])-1] 
				if dc == 2.49:
					d_plus = d_plus + obstacle_distance*7.031
				elif dc == 2.44:
					d_plus = d_plus + obstacle_distance*4.031
				elif dc == 52.7:
					d_plus = d_plus + obstacle_distance*2.183

			# obstacle_time = obstacle_time + obstacle_distance/(c*(1/((obstacles[o][len(obstacles[o])-1])**0.5)))

	return total_distance+d_plus+np.random.normal(0,0.005625)

def estimated_rssi(ap,bp,obstacles):
	total_distance = ((ap['x']-bp['x'])**2+(ap['y']-bp['y'])**2)**0.5
	rssi_drop = 0
	for o in obstacles:
		if obstacles[o]:
			for i in range(0,len(obstacles[o])-2):
				obstacle_distance = ((obstacles[o][1][0]-obstacles[o][0][0])**2+(obstacles[o][1][1]-obstacles[o][0][1])**2)**0.5
				dc = obstacles[o][len(obstacles[o])-1] 
				if dc == 2.49:
					rssi_drop = rssi_drop + obstacle_distance*127.2
				elif dc == 2.44:
					rssi_drop = rssi_drop + obstacle_distance*14.5827
				elif dc == 52.7:
					rssi_drop = rssi_drop + obstacle_distance*63.3707
	return -2.5134*total_distance-66.6-rssi_drop+np.random.normal(0,0.64)



def get_distance(a,bp,obstacles):
	c = 299792458

	distance = estimated_distance(a.get_pos(),bp,obstacles,c)
	rssi = estimated_rssi(a.get_pos(),bp,obstacles)

	return [distance,rssi]

def get_expected_rssi(distance):
	return -2.5134*distance-66.6	
