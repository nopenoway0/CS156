from explorer import *

class Pit():
	def __init__(self):
		pass
	def getString(self):
		return "*"

class Gold():
	def __init__(self):
		pass
	def getString(self):
		return "G"

class Environment():
	def __init__(self, size = 5):
		self.size = size
		self.board = []
		for x in range(0,self.size):
			self.board.append([])
			for y in range(0,self.size):
				self.board[x].append(0)
		self.game_over = False
		self.game_over_m = ""

	def getString(self):
		rep = ""
		for y in reversed(range(0,self.size)):
			for x in range(0,self.size):
				if(isinstance(self.board[x][y], int)):
					rep += str(self.board[x][y]) + " "
				else:
					rep += self.board[x][y].getString() + " "
			rep += "\n"
		return rep

	# Breeze, Smell, Glitter
	def getPercept(self):
		ori_x, ori_y = self.agent.orientation
		breeze, smell, glitter = (False, False, False)
		if((self.agent.x + ori_x) < self.size and (self.agent.x + ori_x) > 0 and (self.agent.y + ori_y) > 0 and (self.agent.y + ori_y) < self.size and isinstance(self.board[self.agent.x + ori_x][self.agent.y + ori_y], Pit)):
			breeze = True
		if((self.agent.x + ori_x) < self.size and (self.agent.x + ori_x) > 0 and (self.agent.y + ori_y) > 0 and (self.agent.y + ori_y) < self.size and isinstance(self.board[self.agent.x + ori_x][self.agent.y + ori_y], Gold)):
			glitter = True
		self.execute_action(self.agent.program(breeze, smell, glitter, (5,5))) 

	def step(self):
		self.getPercept()

	def place_object(self, coordinate, obj):
		x, y = coordinate
		self.board[x][y] = obj
		if(isinstance(obj, Agent)):
			self.agent = obj
			self.agent.x = x
			self.agent.y = y

	def move_object(self, coordinate, obj):
		self.board[obj.x][obj.y] = 0
		x, y = coordinate
		if(isinstance(obj, Agent)):
			if(isinstance(self.board[x][y], Pit)):
				self.game_over = True
				self.game_over_m = "You died!"
				return
			self.agent = obj
			self.agent.x = x
			self.agent.y = y
		self.board[x][y] = obj

	def del_object(self, coordinate):
		self.board[coordinate[0]][coordinate[1]] = 0

	def execute_action(self, action):
		f_x, f_y = self.agent.orientation
		if(action == "forward"):
			#self.agent.x += f_x
			#self.agent.y += f_x
			self.move_object((self.agent.x + f_x, self.agent.y + f_y), self.agent)
		elif(action == "turn left"):
			if(f_x == -1):
				self.agent.changeOrientation((0,-1))
			elif(f_x == 1):
				self.agent.changeOrientation((0, 1))
			elif(f_x == 0 and f_y == 1):
				self.agent.changeOrientation((-1,0))
			else:
				self.agent.changeOrientation((1,0))
		elif(action == "turn right"):
			if(f_x == -1):
				self.agent.changeOrientation((0,1))
			elif(f_x == 1):
				self.agent.changeOrientation((0, -1))
			elif(f_x == 0 and f_y == 1):
				self.agent.changeOrientation((1,0))
			else:
				self.agent.changeOrientation((-1,0))	
		elif(action == "grab"):
			self.del_object((self.agent.x + f_x, self.agent.y + f_y))
			self.game_over = True
			self.game_over_m = "You Won!"
		# add turn right