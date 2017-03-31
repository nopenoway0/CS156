from sympy import *
import re
import random
class Agent():
	def __init__ (self, coordinate = (0,0)):
		self.x, self.y = coordinate

class Explorer(Agent):
	def __init__(self, coordinate = (0,0)):
		self.x, self.y = coordinate
		self.location = (0,0)
		self.orientation = (1,0)
		self.kb = []
		self.statements = []
		self.rule_set = None
		self.rule_set_m = False

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
		#satisfiable(fact[0]) # checks for syntax - terrible way of doing it
		self.kb.append(fact)
		query = ""
		for x in range(0, len(self.kb)):
			if(x > 0):
				query += " & "
			query += self.kb[x]
		#if(len(self.statements) > 0):
		#	tmp = re.split(r'\s+|&|>>|<<|\||(|)', self.statements[0])
		#	print(tmp)
		#if(len(self.kb) > 0):
			#self.rule_set = simplify_logic(query)
		# Hardcoded stuff
		modifiers = (self.x, self.y, self.x, self.y + 1, self.x + 1, self.y, self.x, self.y + 1, self.x + 1, self.y, self.x, self.y)
		base_rule_1 = "B%d%d >> (P%d%d | P%d%d) & (P%d%d | P%d%d) >> B%d%d" % modifiers
		#"B10 >> (P00 | P11 | P20) & (P00 | P11 | P20) >> B10"
		modifiers = (self.x + 1, self.y, self.x, self.y, self.x + 1, self.y + 1, self.x + 2, self.y, self.x, self.y, self.x + 1, self.y + 1, self.x + 2, self.y, self.x + 1, self.y)
		base_rule_2 = "(B%d%d >> (P%d%d | P%d%d | P%d%d)) & ((P%d%d | P%d%d | P%d%d) >> B%d%d)" % modifiers
		self.rule_set = query + " & " + base_rule_1 + " & " + base_rule_2
		self.rule_set_m = True

	def ask(self, question):
		if(self.rule_set_m):
			self.rule_set = to_cnf(self.rule_set)
			self.rule_set_m = False
		#print(self.rule_set)
		#print(satisfiable(self.rule_set))
		return satisfiable(self.rule_set)

	def getFacts(self):
		return self.kb

	def program(self, breeze, smell, glitter, bounds):
		ori_x, ori_y = self.orientation
		bounds_x, bounds_y = bounds
		if(breeze):
			#print("there's a breeze alright")
			self.tell("B%d%d" % (self.x, self.y))
			self.tell("~P%d%d" % (self.x, self.y))
		results = self.ask("test")
		if(isinstance(results, bool)):
			self.rule_set_m = True
			return self.turnRandom()
		#print("Checking: " + "P" + str(self.x + ori_x) + str(self.y + ori_y) + " in " + str(results))
		results = results.items()
		check = "P%d%d" % (self.x + ori_x, self.y + ori_y)
		if(glitter):
			return "grab"
		for [x,y] in results:
			if(check == str(x) and y):
				return self.turnRandom()
		if(self.x == 0 and self.printOrientation() == "left"):
			return "turn right"
		if(self.y == 0 and self.printOrientation() == "down"):
			return self.turnRandom()
		if((self.y == bounds_y - 1 and self.printOrientation() == "up") or (self.x == bounds_x - 1 and self.printOrientation() == "right")):
			return "turn right"
		return "forward"

	def turnRandom(self):
		if(random.randrange(0,2) == 0):
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