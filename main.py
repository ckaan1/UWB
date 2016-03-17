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

	anchors = []
	anchors.append(AnchorNode(0,0,0,0.1))
	anchors.append(AnchorNode(5,0,0,0.1))
	anchors.append(AnchorNode(0,8,0,0.1))
	anchors.append(AnchorNode(5,8,0,0.1))

	beacon = BeaconNode(0.5,0.5,0)

	bp = beacon.getPos()
	print 'Beacon pos: ', bp
	for a in anchors:
		ap = a.getPos()
		print 'Anchor pos: ', ap
		collision = env.determine_NLOS([ap['x'],ap['y']],[bp['x'],bp['y']])
		print collision

	raw_input("Press enter to exit...")
