from sympy import *
import re
import random
import copy
class Agent():
	def __init__ (self, coordinate = (0,0)):
		self.x, self.y = coordinate

# Reflex agent that uses prepositional logic to navigate
class Explorer(Agent):
	def __init__(self, coordinate = (0,0)):
		self.x, self.y = coordinate
		self.location = (0,0)
		self.orientation = (1,0)
		self.kb = []
		# index 0 is Pit related rules and index 1 is Wumpus related
		self.rule_set = []
		self.rule_set_m = False
		self.pits = []
		self.default_ruleset = True
		self.wumpus = None
	# returns string representation of object
	def getString(self):
		if(self.printOrientation() == "left"):
			return "<"
		elif(self.printOrientation() == "right"):
			return ">"
		elif(self.printOrientation() == "up"):
			return "^"
		else:
			return "v"

	# True is general rule - False is specific
	def tell(self, fact):
		self.kb.append(fact) if fact not in self.kb else None
		self.update_rule_set()

	def update_rule_set(self):
		self.rule_set = []
		query = ""
		ori_x, ori_y = self.orientation
		for x in range(0, len(self.kb)):
			if(x > 0):
				query += " & "
			query += self.kb[x]
		modifiers = (self.x, self.y, self.x, self.y + ori_y, self.x + ori_x, self.y, self.x, self.y + ori_y, self.x + ori_x, self.y, self.x, self.y, self.x, self.y, self.x, self.y + ori_y, self.x + ori_x, self.y)

		base_rule_1 = "(B%d%d >> (P%d%d | P%d%d)) & ((P%d%d | P%d%d) >> B%d%d) & (~B%d%d >> ~(P%d%d | P%d%d))" % modifiers
		smell_rule_1 = "(S%d%d >> (W%d%d | W%d%d)) & ((W%d%d | W%d%d) >> S%d%d) & (~S%d%d >> ~(W%d%d | W%d%d))" % modifiers
		
		modifiers = (self.x, self.y, self.x, self.y, self.x + ori_x, self.y + ori_y, self.x + 2, self.y, self.x, self.y, self.x + ori_x, self.y + ori_y, self.x + 2, self.y, self.x, self.y)
		base_rule_2 = "(B%d%d >> (P%d%d | P%d%d | P%d%d)) & ((P%d%d | P%d%d | P%d%d) >> B%d%d)" % modifiers
		smell_rule_2 = "(S%d%d >> (W%d%d | W%d%d | W%d%d)) & ((W%d%d | W%d%d | W%d%d) >> S%d%d)" % modifiers
		self.rule_set.append(query + " & " + base_rule_1 + " & " + base_rule_2)
		self.rule_set . append(query + "  & (" + smell_rule_1 + " & " + smell_rule_2 + ")") 
		self.rule_set_m = True

	def ask(self, question):
		#if(self.rule_set_m):
		if(question == "wumpus"):
			index = 1
		else:
			index = 0
		self.rule_set = to_cnf(self.rule_set[index])

		self.update_rule_set()
		return satisfiable(self.rule_set[index])

	def flush(self):
		self.rule_set[0] = "~P%d%d" % (self.x, self.y)
		self.rule_set[1] = "~W%d%d" % (self.x, self.y)
		self.kb = copy.copy(self.pits)
		if(self.wumpus != None):
			self.kb.append(self.wumpus)

	def getFacts(self):
		return self.kb

	def program(self, breeze, smell, glitter, bounds):
		self.tell("~P%d%d" % (self.x, self.y))
		self.tell("~W%d%d" % (self.x, self.y))
		ori_x, ori_y = self.orientation
		bounds_x, bounds_y = bounds
		if(self.x + ori_x < 0 or self.y + ori_y < 0 or self.x + ori_x > bounds_x or self.y + ori_y > bounds_y):
			return self.turnRandom()
		if(breeze):
			self.tell("B%d%d" % (self.x, self.y))
		else:
			self.tell("~B%d%d" % (self.x, self.y))
		if(smell):
			self.tell("S%d%d" % (self.x, self.y))
		else:
			self.tell("~S%d%d" % (self.x, self.y))
		results_p = self.ask("pit")
		if(isinstance(results_p, bool)):
			print(results_p)
			self.rule_set_m = True
			self.flush()
			results_p = self.ask("pit")
			return "forward"
		results_p = results_p.items()
		check_pit = "P%d%d" % (self.x + ori_x, self.y + ori_y)
		check_wumpus = "W%d%d" % (self.x + ori_x, self.y + ori_y)
		if(glitter):
			return "grab"
		for [x,y] in results_p:
			if(check_pit == str(x) and y):				
				self.pits.append(check_pit) if check_pit not in self.pits else None
				self.tell(check_pit)
				return self.turnRandom()
			if(check_wumpus == str(x) and y):				
				self.wumpus = check_wumpus
				self.tell(check_wumpus)
				return self.turnRandom()		
		if(self.x == 0 and self.printOrientation() == "left"):
			return self.turnRandom()
		if(self.y == 0 and self.printOrientation() == "down"):
			return self.turnRandom()
		if((self.y == bounds_y - 1 and self.printOrientation() == "up") or (self.x == bounds_x - 1 and self.printOrientation() == "right")):
			return self.turnRandom()
		return "forward"

	def turnRandom(self):
		if(random.randrange(1,2) == 0):
			return "turn left"
		else:
			return "turn right"

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