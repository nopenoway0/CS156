import random, copy
import numpy as np
import time

# Objects that stay still
class Object:
	def __init__(self, passable):
		self.passable = None
	def get_picture(self):
		raise NotImplementedError("Picture not implemented")

class Tile(Object):
	# false - dirty : true - clean
	def __init__(self, condition):
		self.condition = condition
		self.passable = True
	def __str__(self):
		return "Tile Object status: " + str(self.condition)
	def set_clean(self):
		self.condition = True
	def set_dirty(self):
		self.condition = False
	def get_picture(self):
		if(self.condition):
			return "O"
		else:
			return "X"

class Wall(Object):
	def __init__(self):
		self.passable = False
	def get_picture(self):
		return "W"

class Agent():
	def __init__(self):
		self.env = None
		env = None
	def start(self):
		raise NotImplemented("Missing start Method")
	def set_env(self, env):
		raise NotImplementedError("Set_Env not implemented")

class ReflexAgent(Agent):
	def __init__(self):
		self.env = None
		env = None
	def set_env(self, env):
		raise NotImplemented("Set_Env not implemented")

class Robot(Object, ReflexAgent):
	def __init__(self):
		self.env = None
		self.x = None
		self.y = None
		self.cur_tile = Tile(True)
	def get_picture(self):
		return "R"	
	def set_env(self, env):	
		if(isinstance(env, Environment)):
			self.env = env
		else:
			raise ReferenceError("Not a valid Environment")
	def start(self):
		cleaned = True
		if(self.env == None or self.y == None or self.x == None):
			raise Exception("Could not get environment")

		# get surrounding blocks
		while(cleaned):
			cleaned = self.check(1, 0)
			if(cleaned == False):
				cleaned = self.check(0,1)
			if(cleaned == False):
				cleaned = self.check(1,1)
			if(cleaned == False):
				cleaned = self.check(0, -1)
			if(cleaned == False):
				cleaned = self.check(1, -1)
			if(cleaned == False):
				cleaned = self.check(-1, -1)
			if(cleaned == False):
				cleaned = self.check(-1, 1)
			if(cleaned == False):
				cleaned = self.check(-1, 0)
			print self.env.get_picture()
			time.sleep(1)

	def check(self, inc_x, inc_y):
			ob = self.env.get_object(self.x + inc_x, self.y + inc_y)
			if(ob.passable == True and ob.condition == False):
				self.env.place_object(self.x, self.y, self.cur_tile)
				self.x += inc_x
				self.y += inc_y
				self.cur_tile = self.env.get_object(self.x, self.y)
				self.env.place_object(self.x, self.y, self)
				cur_tile = ob
				cur_tile.set_clean()
				return True
			else:
				return False

	def set_coord(self, x, y):
		self.x = x
		self.y = y

class Environment:
	def __init__(self):
		self.env = []
	def init(self, width, height):
		# Increment values to account for walls being drawn
		width += 2
		height += 2
		for x in range(0, width):
			self.env.append([])
			for y in range(0, height):
				if(x == 0 or x == width - 1 or y == 0 or y == height - 1):
					self.env[x].append(Wall())
				elif(random.randint(0,2) == 1):
					self.env[x].append(Tile(True))
				else:
					self.env[x].append(Tile(False))
	def get_picture(self):
		picture = ""
		for x in range(0, len(self.env)):
			for y in range(0, len(self.env[x])):
				picture += self.env[x][y].get_picture()
			picture += "\n"
		return picture
	def place_object(self, x, y, object):
		# prevent placement on walls
		if(isinstance(object, Robot)):
			object.set_coord(x, y)
		x += 1
		y += 1
		self.env[x][y] = object
	def get_object(self, x, y):
		return self.env[x + 1][y + 1]

# program starts here
env = Environment()
agent_test = Robot()
env.init(10,5)
env.place_object(0, 0, agent_test)
agent_test.set_env(env)

print env.get_picture()
agent_test.start()
