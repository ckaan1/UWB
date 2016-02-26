import time
import sys
from numpy import *
from anchor_nodes import *
from beacon_node import *
from environment import *
from experiments import *
from localization_algorithms import *
from nlos_detection import *
from sensor_simulation import *

if __name__ == "__main__":

	env = Environment(1)
	print "Boundaries\n", env.boundaries
	print "Obstacles\n", env.obstacles

	p1 = (0.5,0.5)
	p2 = (3.5,7.5)
	print p1,p2
	collisions = env.determine_collision(p1,p2)
	print collisions

	raw_input("Press enter to exit...")
