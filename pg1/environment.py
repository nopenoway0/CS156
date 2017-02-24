# Custom imports
from interfaces import Agent
from interfaces import Object
from interfaces import Metric

# contains agent and rooms
class Environment:
	# intializes all variables to 0 or none1
	def __init__(self):
		self.metric_inc = None
		self.metric_func = None
		self.objects = []
		self.rows = None
		self.columns = None
		self.agent = None
		self.metric_calc = None
		self.data = None
		self.num_dirt = 0

	# Takes a metric function and a metric initializer these will run after every update from the agent
	def initialize_metric(self, metric_func, metric_init, metric_calc):
		self.metric_inc = metric_init()
		self.metric_func = metric_func
		self.metric_calc = metric_calc

	# takes a time and initializes an array of specified length, must be of type object
	def initialize_env(self, rows, columns, type):
		self.rows = rows
		self.columns = columns
		for y in range(0, columns):
			self.objects.append([])
			for x in range(0, rows):
				self.objects[y].append(type())

	# Print all objects in environment
	def toString(self):
		string = ""
		for y in range(0, self.columns):
			for x in range(0, self.rows):
				string += self.objects[y][x].toString()
			string += "\n"
		return string

	# returns objects at specified coordinates
	def getObject(self, x, y):
		if(x > self.rows or y > self.columns):
			return Room()
		return self.objects[y][x]

	# places object at designated coordinates
	def placeObject(self, x, y, repl):
		if(x > self.rows or y > self.columns):
			raise Exception("Out of environment bounds")
		if(isinstance(self.objects[y][x], Room) and self.objects[y][x].validRoom == False):
			raise Exception("Out of environment bounds")
		if(isinstance(repl, Agent)):
			repl.setEnv(x, y, self)
			self.objects[y][x] = repl
			self.agent = repl
			return
		self.objects[y][x] = repl

	# calls changeState funciton of object at specified coordinates
	def changeObjectState(self, x, y, newState):
		if(isinstance(self.objects[y][x], Room) and newState == True and self.objects[y][x].condition == False):
			self.num_dirt = self.num_dirt + 1
		self.objects[y][x].changeState(newState)

	# Starts the agent in the environment
	def stageEnv(self):
		if(self.agent == None):
			raise Exception("No Valid Agent")
		while(self.agent.process()):
			self.metric_inc = self.metric_func(self.agent)	
		return self.metric_calc(self.metric_inc, self.data)

	# Changes data variable that is used in calculating metric
	def alterData(self, param):
		self.data = param

	# returns contents of data variable
	def getData(self):
		return data

	# used to manually set dirty rooms - shouldn't be used as this variable is automatically set
	def setNumDirtyRooms(self, num):
		self.num_dirt = num

	# Returns number of dirty Rooms
	def getNumDirtyRooms(self):
		return self.num_dirt


class Room(Object):
	def __init__(self):
		self.condition = False
		self.validRoom = False

	# Status - False = Dirty - True = Clean
	def set_condition(self, status):
		self.condition = status

	# If room is dirty it will be printed as X if it is clean it is O
	def toString(self):
		picture = ""
		if(self.validRoom == False):
			picture += "."
		elif(self.condition == False):
			picture += "X"
		else:
			picture += "O"
		picture += " "
		return picture

	# If false, is a boundary or wall
	def isPassable(self):
		return self.validRoom

	# Can be used to disable or enable a room. If disabled, will automatically act as a wall
	def changeState(self, newState):
		self.validRoom = newState

	# Returns whether the room is dirty or clean
	def getCondition(self):
		return self.condition