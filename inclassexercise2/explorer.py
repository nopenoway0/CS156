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
		self.moves = 0
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

		if(fact.find("~") == -1):
			checker = "~" + fact
			while(checker in self.kb):
				self.kb.remove(checker)
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

		# RULE SET 1
		base_rule_1 = "(B%d%d >> (P%d%d | P%d%d)) & ((P%d%d | P%d%d) >> B%d%d) & (~B%d%d >> ~(P%d%d | P%d%d))" % modifiers
		smell_rule_1 = "(S%d%d >> (W%d%d | W%d%d)) & ((W%d%d | W%d%d) >> S%d%d) & (~S%d%d >> ~(W%d%d | W%d%d))" % modifiers
		
		# RULE SET 2
		modifiers = (self.x, self.y, self.x, self.y, self.x + ori_x, self.y + ori_y, self.x + 2, self.y, self.x, self.y, self.x + ori_x, self.y + ori_y, self.x + 2, self.y, self.x, self.y)
		base_rule_2 = "(B%d%d >> (P%d%d | P%d%d | P%d%d)) & ((P%d%d | P%d%d | P%d%d) >> B%d%d)" % modifiers
		smell_rule_2 = "(S%d%d >> (W%d%d | W%d%d | W%d%d)) & ((W%d%d | W%d%d | W%d%d) >> S%d%d)" % modifiers
		
		self.rule_set.append(query + " & " + base_rule_1 + " & " + base_rule_2)

		query_2 = ""
		for x in range(0, len(self.kb)):
			if(self.kb[x].find("S") != -1):
				if(x > 0 and len(query_2) > 0):
					query_2 += " & "
				query_2 += self.kb[x]
		self.rule_set.append(query_2 + "  & " + smell_rule_1 + " & " + smell_rule_2) 
		#if(len(query_2) > 0 ):
			#raw_input("Query 2: " + query_2)
		self.rule_set_m = True

	# Checks satisfiabilitty for the requested ruleset with current percepts
	def ask(self, question):
		if(question == "wumpus"):
			index = 1
		else:
			index = 0
		self.rule_set = to_cnf(self.rule_set[index])

		self.update_rule_set()
		return satisfiable(self.rule_set[index])

	# Necessary to flush uneeded data in order to keep program running quickly
	def flush(self):
		self.rule_set[0] = "~P%d%d" % (self.x, self.y)
		self.rule_set[1] = "~W%d%d" % (self.x, self.y)
		self.kb = copy.copy(self.pits)
		if(self.wumpus != None):
			self.kb.append(self.wumpus)
	# Unused
	def getFacts(self):
		return self.kb

	# checks ruleset2 which contains the ruels for checkign if a wumpus exists
	def checkWumpus(self, check_wumpus):
		results = self.ask("wumpus")
		results = results.items()
		for [x,y] in results:
			if(check_wumpus == str(x) and y):	
				self.wumpus = check_wumpus
				self.tell(check_wumpus)
				return self.turnRandom()
		else:
			return "None"

	# The checks are called and the percepts are passed to be checked with the rules
	def program(self, breeze, smell, glitter, bounds):
		self.tell("~P%d%d" % (self.x, self.y))
		self.tell("~W%d%d" % (self.x, self.y))
		ori_x, ori_y = self.orientation
		bounds_x, bounds_y = bounds
		check_pit = "P%d%d" % (self.x + ori_x, self.y + ori_y)
		check_wumpus = "W%d%d" % (self.x + ori_x, self.y + ori_y)

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
		results = self.ask("pit")
		if(isinstance(results, bool)):
			# check for wumpus
			results = self.checkWumpus(check_wumpus)
			self.rule_set_m = True
			self.flush()
			if(results == "None"):
				return "forward"
			else:
				return results
		results = results.items()
		# Check for Gold
		if(glitter):
			return "grab"
		# Check for pit
		for [x,y] in results:
			if(check_pit == str(x) and y):				
				self.pits.append(check_pit) if check_pit not in self.pits else None
				self.tell(check_pit)
				return self.turnRandom()
		# Check for possible Wumpus
		self.checkWumpus(check_wumpus)

		# check for bounds			
		if(self.x == 0 and self.printOrientation() == "left"):
			return self.turnRandom()
		if(self.y == 0 and self.printOrientation() == "down"):
			return self.turnRandom()
		if((self.y == bounds_y - 1 and self.printOrientation() == "up") or (self.x == bounds_x - 1 and self.printOrientation() == "right")):
			return self.turnRandom()
		return "forward"

	# For sake of predictability set to always turn right
	def turnRandom(self):
		if(random.randrange(1,2) == 0):
			return "turn left"
		else:
			return "turn right"

	def changeOrientation(self, orientation):
		self.orientation = orientation

	# returns text rep of orientation
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