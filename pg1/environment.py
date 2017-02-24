# Custom imports
from interfaces import Agent
from interfaces import Object
from interfaces import Metric


class Environment:
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

	def toString(self):
		string = ""
		for y in range(0, self.columns):
			for x in range(0, self.rows):
				string += self.objects[y][x].toString()
			string += "\n"
		return string

	def getObject(self, x, y):
		if(x > self.rows or y > self.columns):
			return Room()
		return self.objects[y][x]

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

	def changeObjectState(self, x, y, newState):
		if(isinstance(self.objects[y][x], Room) and newState == True and self.objects[y][x].condition == False):
			self.num_dirt = self.num_dirt + 1
		self.objects[y][x].changeState(newState)

	def stageEnv(self):
		if(self.agent == None):
			raise Exception("No Valid Agent")
		while(self.agent.process()):
			self.metric_inc = self.metric_func(self.agent)	
		return self.metric_calc(self.metric_inc, self.data)

	def alterData(self, param):
		self.data = param

	def getData(self):
		return data

	def numDirtyRooms(self, num):
		self.num_dirt = num

	def getNumDirtyRooms(self):
		return self.num_dirt

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
			picture += "."
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

	def getCondition(self):
		return self.condition
