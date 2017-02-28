# Custom interfaces
from interfaces import Agent
from interfaces import Object
from interfaces import Metric

#Python library
import os
import time
import sys

class Robot(Agent, Object, Metric):

	# Declares all variables to 0
	def __init__(self, wait_time):
		self.started = False
		self.env = None
		self.current_room = None
		self.x = None
		self.y = None
		self.cleaned_room = 0
		self.wait_time = wait_time
	# Search top -> right -> down -> left
	def process(self):
		flag = False
		try:
			flag = self.checkDirtySquares()
		except Exception as E:
			print(E)
			return False
		return flag

	# Checks 4 directions around self for dirty squares - if it finds one it will vacuum the current square and move to it
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

	# gives the robot an environment, must give environment and its current coordinates withint his environment
	def setEnv(self, x, y, env):
		self.env = env
		self.current_room = self.env.objects[y][x]
		self.x = x
		self.y = y
	def toString(self):
		return "R "

	# defiend as part of object class
	def isPassable(self):
		return False

	# not yet implemented, not yet needed
	def changeState(self):
		pass

	# used to set what the robot believes is the room it is currently present in
	def setRoom(self, room):
		self.current_room = room

	# returns room robot is current in
	def getRoom(self):
		return self.current_room

	# returns number of cleaned rooms - used only for metrics
	def getCleanRooms(self):
		return self.cleaned_room

	# vacuums room and sets it to clean, increments cleaned room variable to be used as a comparison for a metric
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
		# Flush and print
		if(os.name is "posix"):
			os.system("clear")
		else:
			os.system("cls")
		print(self.env.toString())
		#
		time.sleep(self.wait_time)

	# returns cleaned rooms to the metric variable in the environment that is calling it
	@staticmethod
	def metric_func(metric):
		if(isinstance(metric, Robot)):
			return metric.getCleanRooms()
		else:
			raise Exception("Invalid metric object")
	
	# Currently unused
	@staticmethod
	def init_metric():
		return 0

	# where data is the number of dirty rooms and the metric is the rooms cleaned. Will be called once agent tells the enviornment it has finished
	@staticmethod
	def calc_metric(metric, data):
		if(metric > 0 and metric < data):
			metric = metric + 1
		#if(metric > data):
			#raise Exception("Invalid Metric Measurement - Either corrupt data was used or metric wasn't finished")
		#else:
		result = data - metric
		if(data == 0):
			print("No rooms to clean")
			return 0
		elif(metric < data):
			print("Cleaned " + str(metric) + " out of " + str(data) + " rooms. Incomplete.")
		elif(metric == data):
			print("Cleaned all " + str(data) + " rooms. Completed Run.")
		else:
			while(metric > data):
				metric = metric - 1
			print("cleaned " + str(metric) + " rooms out of " + str(data))
		return result
