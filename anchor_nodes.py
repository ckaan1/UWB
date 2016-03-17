class AnchorNode:
	def __init__(self,x,y,z,variance):
		self.pos = {'x':x,'y':y,'z':z}
		self.v = variance

	def getPos(self):
		return self.pos
