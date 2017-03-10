import cs156_logic as cl

def wumpus1():
	print("\nWumpus 1 start\n")
	kb = cl.PropKB()
	kb.tell(cl.expr("~P11"))
	kb.tell(cl.expr("B11 <=> (P12 | P21)"))
	kb.tell(cl.expr("B21 <=> (P11 | P22 | P31)"))
	kb.tell(cl.expr("~B11"))
	kb.tell(cl.expr("B21"))

	print("Printing clauses from wumpus1: " + str(kb.clauses))

wumpus1()