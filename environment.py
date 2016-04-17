####################################################################
##
## Environment creation class
## Creates an environment with set size
## Can define different environments based on pre-designed settings
## Will also be able to determine if a path is in collision
##
####################################################################
import matplotlib.patches as ptc
import matplotlib.pyplot as plt

class Environment:
	def __init__(self,environment_number):
		self.boundaries = {'x':[0, 10],'y':[0, 10]}
		self.obstacles = get_obstacles( environment_number )

	## Determine if there is a NLOS condition between to radios
	def determine_NLOS( self, p1, p2 ):
		collisions = {}
		for o in self.obstacles:
			collisions[o] = []
			if( (p1[0]==p2[0]) and (p1[1]==p2[1])):
				continue
			else:
				# Determine obstacle bounds
				# x = x_min
				ol1 = self.obstacles[o]['x'][0]
				# y = y_min
				ol2 = self.obstacles[o]['y'][0]
				# x = x_max
				ol3 = self.obstacles[o]['x'][1]
				# y = y_max
				ol4 = self.obstacles[o]['y'][1]

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

				# Create list of intersection of lines
				points = [(x_min,ol2),(ol1,y_min),(x_max,ol4),(ol3,y_max)]

				# Check if the points created are in collision with the obstacle
				for p in points:
					dist1 = ((p1[0]-p[0])**2+(p1[1]-p[1])**2)**0.5
					dist2 = ((p2[0]-p[0])**2+(p2[1]-p[1])**2)**0.5
					tdist = ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

					# Make sure that the intersection point does not extend past the two points given
					if (dist1 > tdist) or (dist2 > tdist):
						if dist1 > dist2:
							p = (p2[0],p2[1])
						else:
							p = (p1[0],p1[1])

					# Check if updated intersection points are in an obstacle
					if( (p[0]>=(ol1-0.001) and p[0]<=(ol3+0.001)) and (p[1]>=(ol2-0.001) and p[1]<=(ol4+0.001)) ):
						collisions[o].append((p[0],p[1]))
				if( collisions[o] ):
					collisions[o].append(self.obstacles[o]['dc'])
		
		# Return list of obstacles that blocked p1 and p2
		return collisions

	def in_obstacle(self,pos):
		for o in self.obstacles:
			# x = x_min
			ol1 = self.obstacles[o]['x'][0]
			# y = y_min
			ol2 = self.obstacles[o]['y'][0]
			# x = x_max
			ol3 = self.obstacles[o]['x'][1]
			# y = y_max
			ol4 = self.obstacles[o]['y'][1]

			if( (pos[0]>=ol1 and pos[0]<=ol3) and (pos[1]>=ol2 and pos[1]<=ol4) ):
				return True
		return False

	def draw_obstacles(self):
		fig = plt.figure()
		ax1 = fig.add_subplot(111,aspect='equal')
		for o in self.obstacles:
			ol1 = self.obstacles[o]['x'][0]
			ol2 = self.obstacles[o]['y'][0]
			ol3 = self.obstacles[o]['x'][1]
			ol4 = self.obstacles[o]['y'][1]

			p = ptc.Rectangle((ol1,ol2),ol3-ol1,ol4-ol2,edgecolor="#00ff00",facecolor='#00ff00')
			ax1.add_patch(p)



## Assume rectangular obstacles that are aligned with x and y axis for now
#  An obstacle is defined as 
#  x: [x_min, x_max]
#  y: [y_min, y_max]
#  dc: dielectric constant of the material
#  An environment_number of 0 or a number that is not defined will return no obstacles
def get_obstacles( environment_number ):
	if environment_number==0:
		obstacles = {}
		return obstacles		
	elif environment_number==1:
		obstacles = {}
		obstacles[0] = {'x':[1, 2],'y':[1, 3],'dc':1.55}
		obstacles[1] = {'x':[1.5, 4.5],'y':[6.0, 7.0],'dc':1.2}
		return obstacles
	elif environment_number==2:
		obstacles = {}
		obstacles[0] = {'x':[4,4.00635],'y':[0,4],'dc':2.44}
		obstacles[1] = {'x':[4.00635,4.01905],'y':[0,4],'dc':2.49}
		obstacles[2] = {'x':[4.01905,4.0254],'y':[0,4],'dc':2.44}
		obstacles[3] = {'x':[0,2],'y':[4,4.00635],'dc':2.44}
		obstacles[4] = {'x':[0,2],'y':[4.00635,4.01905],'dc':2.49}
		obstacles[5] = {'x':[0,2],'y':[4.01905,4.0254],'dc':2.44}  
		obstacles[6] = {'x':[3,4.0254],'y':[4,4.00635],'dc':2.44}
		obstacles[7] = {'x':[3,4.0254],'y':[4.00635,4.01905],'dc':2.49}
		obstacles[8] = {'x':[3,4.0254],'y':[4.01905,4.0254],'dc':2.44}  
		obstacles[9] = {'x':[0,2],'y':[6,6.00635],'dc':2.44}
		obstacles[10] = {'x':[0,2],'y':[6.00635,6.01905],'dc':2.49}
		obstacles[11] = {'x':[0,2],'y':[6.01905,6.0254],'dc':2.44}  
		obstacles[12] = {'x':[5,5.00635],'y':[8,10],'dc':2.44}
		obstacles[13] = {'x':[5.00635,5.01905],'y':[8,10],'dc':2.49}
		obstacles[14] = {'x':[5.01905,5.0254],'y':[8,10],'dc':2.44}
		obstacles[15] = {'x':[6,6.2],'y':[2,2.4],'dc':52.7}
		obstacles[16] = {'x':[7,7.2],'y':[2,2.4],'dc':52.7}
		obstacles[17] = {'x':[6.3,6.7],'y':[3,3.2],'dc':52.7}
		return obstacles
	else:
		obstacles = {}
		return obstacles


