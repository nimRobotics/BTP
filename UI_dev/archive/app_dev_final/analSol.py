import numpy as np

class link(object):
	"""finds parameters like mass, inertia of each link"""
	def __init__(self, dim, rho):
		self.l = dim[0]
		self.b = dim[1]
		self.w = dim[2]
		self.rho = rho

	def mass(self):
		"""
		finds mass of a link
		"""
		return self.l*self.b*self.w*self.rho

	def inertia(self,flag=None):
		"""
		calculates inertia of cuboid block 
		flag=0 or None: inertia at mid
		flag=1: inertia at end
		"""
		if flag==0 or flag==None:
			return (self.mass()*(self.l**2))/12
		elif flag==1:
			return (self.mass()*(self.l**2))/3
		else:
			raise ValueError("Unknown flag for finding inertia")

def sliderCrank(dim1, dim2, rho, g):
	l1=link(dim1,rho)
	l2=link(dim2,rho)
	print(l1.mass())
	print(l1.inertia(1))
	print(l2.mass())
	print(l2.inertia())

def fourbar():
	pass

def sixbar():
	pass

sliderCrank([1,2,3],[4,5,6],rho=200,g=9.5)
