import numpy as np

def true_time(ap,bp,obstacles,c):

	total_distance = ((ap['x']-bp['x'])**2+(ap['y']-bp['y'])**2)**0.5
	obstacle_time = 0
	obstacle_distance = 0
	for o in obstacles:
		if obstacles[o]:
			for i in range(0,len(obstacles[o])-2):
				obstacle_distance = obstacle_distance + ((obstacles[o][1][0]-obstacles[o][0][0])**2+(obstacles[o][1][1]-obstacles[o][0][1])**2)**0.5
			obstacle_time = obstacle_time + obstacle_distance/(c*(1/((obstacles[o][len(obstacles[o])-1])**0.5)))

	open_air_time = (total_distance-obstacle_distance)/c

	return open_air_time+obstacle_time

def get_distance(a,bp,obstacles):
	c = 299792458

	total_time = true_time(a.get_pos(),bp,obstacles,c)

	return (c*total_time + np.random.normal(0,a.v))