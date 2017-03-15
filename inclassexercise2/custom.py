import cs156_logic as cl

def wumpus1():
	print("\nWumpus 1 start\n")
	kb = cl.PropKB()
	# Rule 1 - 5
	kb.tell(cl.expr("~P11"))
	kb.tell(cl.expr("B11 <=> (P12 | P21)"))
	kb.tell(cl.expr("B21 <=> (P11 | P22 | P31)"))
	kb.tell(cl.expr("~B11"))
	kb.tell(cl.expr("B21"))


	# Rule 6 - 10
	kb.tell(cl.expr("B11 >> (P12 | P21) & ((P12 | P21)) >> B11"))
	kb.tell(cl.expr("((P12 | P21) >> B11)"))
	kb.tell(cl.expr("~B11 >> ~(P12 | P21)"))
	kb.tell(cl.expr("~(P12 | P21)"))
	kb.tell(cl.expr("~P12 & ~P21"))
	# Rule 11 - 15
	kb.tell(cl.expr("~B12"))
	kb.tell(cl.expr("B12 <=> (P11 | P22 | P13)"))
	kb.tell(cl.expr("~P22"))
	kb.tell(cl.expr("~P13"))
	return kb

def tests(kb):
	test_var = "P"
	coordinate = None
	grid = ""
	line = ""
	for y in range(1,4):
		line = ""
		for x in range(1,4):
			coordinate = test_var + str(x) + str(y)
			if(kb.ask(cl.expr(coordinate)) == {}):
				line += " O"
			elif(kb.ask(cl.expr("B" + str(x) + str(y))) == {}):
				line += " B"
			else:
				line += " ."
		grid = line + "\n" + grid
	return grid


# Main Method
kb = wumpus1()
#print("Printing all rules from wumpus1: " + str(kb.clauses))
print(tests(kb))