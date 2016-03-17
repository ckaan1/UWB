from numpy import *

def true_time(ap,bp,obstacles,dc,c):
	min_x = min(ap['x'],bp['x'])
	min_y = min(ap['y'],bp['y'])
	max_x = max(ap['x'],bp['x'])
	max_y = max(ap['y'],bp['y'])

	total_distance = ((min_x-max_x)**2+(min_y-max_y)**2)**0.5
	obstacle_distance = 0
	for o in obstacles:
		if obstacles[o]:
			obstacle_distance = obstacle_distance + ((obstacles[o][1][0]-obstacles[o][0][0])**2+(obstacles[o][1][1]-obstacles[o][0][1])**2)**0.5

	open_air_time = (total_distance-obstacle_distance)/c
	obstacle_time = obstacle_distance/(c*(1/((dc)**0.5)))

	return open_air_time+obstacle_time

def get_distance(a,bp,obstacles,dc):
	c = 299792458

	total_time = true_time(a.get_pos(),bp,obstacles,dc,c)

	return (c*total_time + random.normal(0,a.v))