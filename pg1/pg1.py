def init_message():
	print("**********************************\n")
	print("****** X is a dirty room**********\n")
	print("****** O is a clean room**********\n")
	print("**********************************\n")

class Metric:
	@staticmethod
	def metric_func(metric):
		raise NotImplementedError("Metric Not Implemented")
	
	@staticmethod
	def init_metric(metric):
		raise NotImplemented("No metric initializer")

class Object:
	def toString(self):
		raise NotImplementedError("No to string method")
	def isPassable(self):
		raise NotImplementedError("Passable not implemented")
	def changeState(self):
		raise NotImplementedError("No change state function")

class Agent:
	def process(self):
		raise NotImplementedError("Not process function")
	def start(self):
		raise NotImplementedError("No start function")
	def stop(self):
		raise NotImplementedError("No start function")
	def setEnv(self, env):
		raise NotImplementedError("No setEnv function")

class Robot(Agent, Object):
	def __init__(self):
		self.started = False
	def process(self):
		pass
	def start(self):
		pass
	def stop(self):
		pass
	def setEnv(self, env):
		pass
	def toString(self):
		pass
	def isPassable(self):
		return False
	def changeState(self):
		pass
		
class Room(Object):
	def __init__(self):
		self.condition = False
		self.validRoom = False
	def set_condition(self, status):
		# Status - False = Dirty - True = Clean
		self.condition = status
	def toString(self):
		picture = ""
		if(self.validRoom == False):
			picture += " "
		elif(self.condition == False):
			picture += "X"
		else:
			picture += "O"
		picture += " "
		return picture
	def isPassable(self):
		return self.validRoom
	def changeState(self, newState):
		self.validRoom = newState

class Environment:
	def __init__(self):
		self.metric_inc = None
		self.metric_func = None
		self.objects = []
		self.rows = None
		self.columns = None
	# Takes a metric function and a metric initializer these will run after every update from the agent
	def initialize_metric(self, metric_func, metric_init):
		self.metric_inc = metric_init()
		self.metric_func = metric_func
	# takes a time and initializes an array of specified length, must be of type object
	def initialize_env(self, rows, columns, type):
		self.rows = rows
		self.columns = columns
		for x in range(0, rows):
			self.objects.append([])
			for y in range(0, columns):
				self.objects[x].append(type())
	def toString(self):
		string = ""
		for x in range(0, self.rows):
			for y in range(0, self.columns):
				string += self.objects[x][y].toString()
			string += "\n"
		return string
	def placeObject(self, x, y, repl):
		if(x > self.rows or y > self.columns):
			raise Exception("Out of environment bounds")
		self.objects[x][y] = repl
	def changeObjectState(self, x, y, newState):
		self.objects[x][y].changeState(newState)
#***********************************************MAIN METHOD*************************************************************************************************************************#
init_message()
env = Environment()
env.initialize_env(5, 5, Room)

# Build rooms
env.changeObjectState(3,4, True)
env.changeObjectState(2,4, True)
env.changeObjectState(2,3, True)
env.changeObjectState(2,2, True)
env.changeObjectState(3,2, True)

print(env.toString())

