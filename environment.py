####################################################################
##
## Environment creation class
## Creates an environment with set size
## Can define different environments based on pre-designed settings
## Will also be able to determine if a path is in collision
##
####################################################################
class Environment:
	def __init__(self,environment_number,dielectric_constant):
		self.boundaries = {'x':[0, 5],'y':[0, 8]}
		self.obstacles = get_obstacles( environment_number )
		self.dielectric = dielectric_constant

	## Determine if there is a NLOS condition between to radios
	def determine_NLOS( self, p1, p2 ):
		collisions = {}
		for o in self.obstacles:
			collisions[o] = []
			# Determine obstacle bounds
			# x = x_min
			ol1 = self.obstacles[o][0]
			# y = y_min
			ol2 = self.obstacles[o][1]
			# x = x_max
			ol3 = self.obstacles[o][2]
			# y = y_max
			ol4 = self.obstacles[o][3]

			# Determine the min and maximum intersections for both x and y
			# 3 different configurations for p1 and p2: Horizontal, Vertical, and Sloped
			# Need to make sure that the intersection exists between p1 and p2
			# If an intersection doesn't actually exist between p1 and p2, the 
			# intersection will be either p1 or p2

			# Horizontal line
			if( p2[1]-p1[1] == 0 ):
				y_min = p2[1]
				y_max = p2[1]
				x_min = min( p1[0],p2[0] )
				x_max = max( p1[0],p2[0] )
			# Vertical line
			elif( p2[0]-p1[0] == 0 ):
				y_min = min( p1[1],p2[1] )
				y_max = max( p1[1],p2[1] )
				x_min = p2[0]
				x_max = p2[0]
			# SLoped line
			else:
				# Slope and y-intersect for the line
				slope = (p2[1]-p1[1])/(p2[0]-p1[0])
				y_int = p2[1] - slope*p2[0]

				y_min = slope*ol1 + y_int
				y_max = slope*ol3 + y_int

				x_min = (ol2-y_int)/slope
				x_max = (ol4-y_int)/slope

			# Determine the points of collision with the obstacle
			# If no collision with obstacle the point will be either p1 or p2
			points = [(x_min,ol2),(ol1,y_min),(x_max,ol4),(ol3,y_max)]

			# Check if the points determined are in the obstacle
			for p in points:
				if ((p[0] > max(p1[0],p2[0])) and (p[1] > max(p1[1],p2[1]))):
					p = ( max(p1[0],p2[0]),max(p1[1],p2[1]) )
				if ((p[0] < min(p1[0],p2[0])) and (p[1] < min(p1[1],p2[1]))):
					p = ( min(p1[0],p2[0]),min(p1[1],p2[1]) )
				# If they are, p1 and p2 are in NLOS, so add the obstacle that blocked it to the list
				if( (p[0]>=ol1 and p[0]<=ol3) and (p[1]>=ol2 and p[1]<=ol4) ):
					collisions[o].append((p[0],p[1]))
		
		# Return list of obstacles that blocked p1 and p2
		return collisions

	def in_obstacle(self,pos):
		for o in self.obstacles:
			# x = x_min
			ol1 = self.obstacles[o][0]
			# y = y_min
			ol2 = self.obstacles[o][1]
			# x = x_max
			ol3 = self.obstacles[o][2]
			# y = y_max
			ol4 = self.obstacles[o][3]

			if( (pos[0]>=ol1 and pos[0]<=ol3) and (pos[1]>=ol2 and pos[1]<=ol4) ):
				return True
			else:
				return False



## Assume rectangular obstacles that are aligned with x and y axis for now
#  An obstacle is defined as [min_x, min_y, max_x, max_y]
#  An environment_number of 0 or a number that is not defined will return no obstacles
def get_obstacles( environment_number ):
	if environment_number==0:
		obstacles = {}
		return obstacles		
	elif environment_number==1:
		obstacles = {}
		obstacles[0] = [1, 1, 2, 3]
		obstacles[1] = [1.5, 6.5, 4.5, 7.0]
		return obstacles
	else:
		obstacles = {}
		return obstacles


