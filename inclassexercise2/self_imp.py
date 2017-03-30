from sympy import *

class Agent():
	def __init__ (self, coordinate = (0,0)):
		self.x, self.y = coordinate

class Explorer(Agent):
	def __init__(self, coordinate = (1,1)):
		self.x, self.y = coordinate
		self.location = (0,0)
		self.orientation = (1,0)

	def getString(self):
		if(self.printOrientation() == "left"):
			return "<"
		elif(self.printOrientation() == "right"):
			return ">"
		elif(self.printOrientation() == "up"):
			return "^"
		else:
			return "V"

	def changeOrientation(self, orientation):
		self.orientation = orientation

	def printOrientation(self):
		x, y = self.orientation
		if(x == 1 and y == 0):
			return "right"
		elif(x == 0 and y == 1):
			return "up"
		elif(x == -1 and y == 0):
			return "left"
		elif(x == 0 and y == -1):
			return "down"
		else:
			return "error"
class Environment():
	def __init__(self, size = 5):
		self.size = size
		self.board = []
		for x in range(0,self.size):
			self.board.append([])
			for y in range(0,self.size):
				self.board[x].append(0)

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

	def getPercept(self):
		pass

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
		self.board[x][y] = obj
		if(isinstance(obj, Agent)):
			self.agent = obj
			self.agent.x = x
			self.agent.y = y

	def execute_action(self, action):
		if(action == "forward"):
			f_x, f_y = self.agent.orientation
			#self.agent.x += f_x
			#self.agent.y += f_x
			self.move_object((self.agent.x + f_x, self.agent.y + f_y), self.agent)
		elif(action == "turn left"):
			f_x, f_y = self.agent.orientation
			if(f_x == -1):
				self.agent.changeOrientation((0,-1))
			elif(f_x == 1):
				self.agent.changeOrientation((0, 1))
			elif(f_x == 0 and f_y == 1):
				self.agent.changeOrientation((-1,0))
			else:
				self.agent.changeOrientation((1,0))
		# add turn right

##### Main #####

board = Environment()
board.place_object((2,2), Explorer())

#print(board.getString())
#board.execute_action("forward")
#print(board.agent.printOrientation())
#print(board.getString())

for x in range(0,4):
	board.execute_action("forward")
	print("going forward 1")
	print(board.getString())
	board.execute_action("turn left")
	print("turning left")
	print(board.getString())

