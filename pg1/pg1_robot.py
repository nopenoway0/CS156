# Custom interfaces
from interfaces import Agent
from interfaces import Object
from interfaces import Metric

#Python library
import os
import time
import sys

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
		flag = False
		try:
			flag = self.checkDirtySquares()
		except Exception as E:
			print(E)
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

	def getCleanRooms(self):
		return self.cleaned_room

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
		time.sleep(1)

	@staticmethod
	def metric_func(metric):
		if(isinstance(metric, Robot)):
			return metric.getCleanRooms()
		else:
			raise Exception("Invalid metric object")
	
	@staticmethod
	def init_metric():
		return 0

	# where data is the number of dirty rooms
	@staticmethod
	def calc_metric(metric, data):
		metric = metric + 1
		if(metric > data):
			raise Exception("Invalid Metric Measurement - Either corrupt data was used or metric wasn't finished")
		else:
			result = data - metric
			if(metric < data):
				print("Cleaned " + str(metric) + " out of " + str(data) + " rooms. Incomplete.")
			elif(metric == data):
				print("Cleaned all " + str(data) + " rooms. Completed Run.")
			return result
