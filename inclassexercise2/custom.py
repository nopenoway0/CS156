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
	kb.tell(cl.expr("P11 | P22 | P13"))
	return kb

def tests(kb):
	pass#print("Asking if P11: " + kb.ask(P11))

# Main Method
kb = wumpus1()
print("Printing all rules from wumpus1: " + str(kb.clauses))
tests(kb)