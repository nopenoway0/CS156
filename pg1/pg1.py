import time
import sys
from math import sqrt
import copy

def init_message():
	print("**********************************\n")
	print("****** X is a dirty room**********\n")
	print("****** O is a clean room**********\n")
	print("**********************************\n")

def exit_message(data):
	print("\nPerformance is: " + str(data) + "\nResults are measured from 0 - 10.\n10 efficiency 0 least")

class Metric:
	@staticmethod
	def metric_func(metric):
		raise NotImplementedError("Metric Not Implemented")
	
	@staticmethod
	def init_metric(metric):
		raise NotImplementedError("No metric initializer")

	@staticmethod
	def calc_metric(metric, data):
		raise NotImplementedError("No metric calculator implemented")

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

class Robot(Agent, Object, Metric):
	def __init__(self):
		self.started = False
		self.env = None
		self.current_room = None
		self.x = None
		self.y = None
		self.cleaned_room = 0
	# Search top -> right -> down -> left
	def process(self):
		#time.sleep(1)
		try:
			flag = self.checkDirtySquares()

			#make pass through environment
			if(self.cleaned_room < self.env.getNumDirtyRooms() and flag == False):
				flag = True
				if(self.env.getObject(self.x, self.y - 1).isPassable()):
					while(self.env.getObject(self.x, self.y - 1).isPassable()):
						if(self.checkDirtySquares() == False and self.cleaned_room < self.env.getNumDirtyRooms()):
							self.move(self.x, self.y - 1)
						else:
							return True
				# check right
				elif(self.env.getObject(self.x + 1, self.y).isPassable()):
					while(self.env.getObject(self.x + 1, self.y).isPassable()):
						if(self.checkDirtySquares() == False):
							self.move(self.x + 1, self.y)
						else:
							return True
				# check below
				elif(self.env.getObject(self.x, self.y + 1).isPassable()):
					while(self.env.getObject(self.x, self.y + 1).isPassable()):
						if(self.checkDirtySquares() == False and self.cleaned_room < self.env.getNumDirtyRooms()):
							self.move(self.x, self.y + 1)
						else:
							return True
				# check left
				elif(self.env.getObject(self.x - 1, self.y).isPassable()):
					while(self.env.getObject(self.x - 1, self.y).isPassable()):
						if(self.checkDirtySquares() == False and self.cleaned_room < self.env.getNumDirtyRooms()):
							self.move(self.x - 1, self.y)
						else:
							return True
				else:
					flag = False	
		except(Exception):
			return False
		return flag

	def checkDirtySquares(self):
		if(self.env.getObject(self.x, self.y - 1).getCondition() is False and self.env.getObject(self.x, self.y - 1).isPassable()):
			self.move(self.x, self.y - 1)
		# check right
		elif(self.env.getObject(self.x + 1, self.y).getCondition() is False and self.env.getObject(self.x + 1, self.y).isPassable()):
			self.move(self.x + 1, self.y)
		# check below
		elif(self.env.getObject(self.x, self.y + 1).getCondition() is False and self.env.getObject(self.x, self.y + 1).isPassable()):
			self.move(self.x, self.y + 1)
		# check left
		elif(self.env.getObject(self.x - 1, self.y).getCondition() is False and self.env.getObject(self.x - 1, self.y).isPassable()):
			self.move(self.x - 1, self.y)
		else:
			return False
		return True

	def start(self):
		pass

	def stop(self):
		pass

	def setEnv(self, x, y, env):
		self.env = env
		self.current_room = self.env.objects[y][x]
		self.x = x
		self.y = y
	def toString(self):
		return "R "

	def isPassable(self):
		return False

	def changeState(self):
		pass

	def setRoom(self, room):
		self.current_room = room

	def getRoom(self):
		return self.current_room

	def suck(self):
		if(self.current_room.getCondition() == False):
			self.current_room.set_condition(True)
			self.cleaned_room = self.cleaned_room + 1
			print(self.cleaned_room)

	def move(self, x, y):
		self.suck()
		self.env.placeObject(self.x, self.y, self.current_room)
		self.suck()
		self.env.placeObject(x, y, self)
		self.x = x
		self.y = y
		print(self.env.toString())
		time.sleep(1)

	@staticmethod
	def metric_func(metric):
		return metric + 1
	
	@staticmethod
	def init_metric():
		return 1

	# where data is the number of dirty rooms
	@staticmethod
	def calc_metric(metric, data):
		metric = metric - 1
		result = (float(data) / metric) * 10.0
		if(result > 10 or metric < data):
			raise Exception("Invalid Metric Measurement - Either corrupt data was used or metric wasn't finished")
		else:
			return result

class MemoryObj:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def getY(self):
		return self.y

	def getX(self):
		return self.x
	def setInfo(self, x, y):
		# add error check
		self.x = x
		self.y = y

class AdvancedRobot(Robot):
	def __init__(self):
		Robot.__init__(self)
		self.memory = []

	def heuristic(self, old_x, old_y, x, y):
		x_diff = old_x - x
		y_diff = old_y - y
		return sqrt(x_diff*x_diff + y_diff*y_diff)

	def checkComplete(self):
		if(self.env.getNumDirtyRooms() <= 0):
			return True
		else:
			return False

	def process(self):
		#time.sleep(1) moved to "move" in robot
		flag = 0
		if(len(self.memory) > 0 and self.x == self.memory[len(self.memory) - 1].getX() and self.y == self.memory[len(self.memory) - 1].getY()):
			# remove memory module
			self.memory.pop()
		x_mod = 0
		y_mod = 0
		if(self.checkComplete()):
			return False
		try:
		# check top
			if(self.env.getObject(self.x, self.y - 1).getCondition() is False and self.env.getObject(self.x, self.y - 1).isPassable()):
				#self.move(self.x, self.y - 1)
				flag += 1
			# check right
			if(self.env.getObject(self.x + 1, self.y).getCondition() is False and self.env.getObject(self.x + 1, self.y).isPassable()):
				#self.move(self.x + 1, self.y)
				flag += 1
			# check below
			if(self.env.getObject(self.x, self.y + 1).getCondition() is False and self.env.getObject(self.x, self.y + 1).isPassable()):
				#self.move(self.x, self.y + 1)
				flag += 1
			# check left
			if(self.env.getObject(self.x - 1, self.y).getCondition() is False and self.env.getObject(self.x - 1, self.y).isPassable()):
				#self.move(self.x - 1, self.y)
				flag += 1
			if(flag == 0 and len(self.memory) == 0):
				return False
			elif(flag > 1):
				self.memory.append(MemoryObj(self.x, self.y))
			elif(flag == 0 and len(self.memory) > 0):
				#find way back to latest memory
				last_mem = self.memory[len(self.memory) - 1]
				option = []
				# add all possible options
				option.append(self.heuristic(self.x, self.y - 1, last_mem.getX(), last_mem.getY()))
				option.append(self.heuristic(self.x + 1, self.y, last_mem.getX(), last_mem.getY()))
				option.append(self.heuristic(self.x, self.y + 1, last_mem.getX(), last_mem.getY()))
				option.append(self.heuristic(self.x - 1, self.y, last_mem.getX(), last_mem.getY()))
				best_option = 100
				if(self.env.getObject(self.x, self.y - 1).isPassable() == False):
					option[0] += 100
				else:
					best_option = option[0]
				if(self.env.getObject(self.x + 1, self.y).isPassable() == False):
					option[1] += 100
				else:
					if(option[1] < best_option):
						best_option = option[1]
				if(self.env.getObject(self.x, self.y + 1).isPassable() == False):
					option[2] += 100
				else:
					if(option[2] < best_option):
						best_option = option[2]
				if(self.env.getObject(self.x - 1, self.y).isPassable() == False):
					option[3] += 100
				else:
					if(option[3] < best_option):
						best_option = option[3]

				# pick lowest cost path as designated by best_option
				for x in range(0, 4):
					if(best_option == option[x]):
						if(x == 0):
							y_mod = -1
						elif(x == 1):
							x_mod = 1
						elif(x == 2):
							y_mod = 1
						elif(x == 3):
							x_mod = -1
				self.move(self.x + x_mod, self.y + y_mod)
				return True

			# check top
			if(self.checkComplete()):
				return False
			if(self.env.getObject(self.x, self.y - 1).getCondition() is False and self.env.getObject(self.x, self.y - 1).isPassable()):
				y_mod = -1
			# check right
			elif(self.env.getObject(self.x + 1, self.y).getCondition() is False and self.env.getObject(self.x + 1, self.y).isPassable()):
				x_mod = 1
			# check below
			elif(self.env.getObject(self.x, self.y + 1).getCondition() is False and self.env.getObject(self.x, self.y + 1).isPassable()):
				y_mod = 1
			# check left
			elif(self.env.getObject(self.x - 1, self.y).getCondition() is False and self.env.getObject(self.x - 1, self.y).isPassable()):
				x_mod = -1
			self.move(self.x + x_mod, self.y + y_mod)
		except(Exception):
			return False
		return True
	@staticmethod
	def calc_metric(metric, data):
		return metric

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
			if(self.metric_func != None):
				self.metric_inc = self.metric_func(self.metric_inc)
				#print(self.toString()) moved to the agent move function
			self.agent = repl
			return
		self.objects[y][x] = repl

	def changeObjectState(self, x, y, newState):
		self.objects[y][x].changeState(newState)

	def stageEnv(self):
		if(self.agent == None):
			raise Exception("No Valid Agent")
		while(self.agent.process()):
			pass	
		return self.metric_calc(self.metric_inc, self.data)

	def alterData(self, param):
		self.data = param

	def getData(self):
		return data

	def numDirtyRooms(self, num):
		self.num_dirt = num

	def getNumDirtyRooms(self):
		return self.num_dirt
#***********************************************MAIN METHOD*************************************************************************************************************************#
# Welcome Message
init_message()

# Create Empty Environment
env = Environment()
# Initiliaze enviornment with size and object classes
env.initialize_env(4, 4, Room)

# Create Robot Agent
rb = Robot()

env.changeObjectState(0,0, True)
env.changeObjectState(1,0, True)
# set number of dirty rooms
env.numDirtyRooms(2)
env.alterData(2)

# Place Robot
env.placeObject(0, 0, rb)

# Set up all metrics
env.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

# Start Simulation - output is performance metric
performance = env.stageEnv()

# Produce Metric Information
exit_message(performance)