class BeaconNode:
	def __init__(self,x,y,z):
		self.pos = {'x':x,'y':y,'z':z}

	def getPos(self):
		return self.pos

	def movePos(self,x,y,z):
		self.pos['x'] = x
		self.pos['y'] = y
		self.pos['z'] = z