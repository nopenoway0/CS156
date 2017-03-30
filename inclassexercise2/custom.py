import cs156_logic as cl
import agents as age

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
print("Started")
env = []
env.append(age.WumpusEnvironment())
env[0].add_object(age.Gold(), (2,2))
env[0].add_object(age.Wumpus(), (3,3))
expl = cl.PLWumpusAgent()
age.test_agent(cl.PLWumpusAgent, 1000, env)
print("End")

