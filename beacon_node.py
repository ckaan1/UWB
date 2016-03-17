class BeaconNode:
	def __init__(self,x,y,z):
		self.pos = {'x':x,'y':y,'z':z}

	def get_pos(self):
		return self.pos

	def move_pos(self,x,y,z):
		self.pos['x'] = x
		self.pos['y'] = y
		self.pos['z'] = z