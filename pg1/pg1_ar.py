
# Custom interfaces
from interfaces import Agent
from interfaces import Object
from interfaces import Metric
from pg1_robot import Robot

#Python library
import time
import sys
from math import sqrt
import copy
import os

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