from sympy import *
import os
from explorer import Explorer, Agent
from environment import Environment, Pit, Gold
import time

##### Main #####

board = Environment()
player = Explorer()

#test = "A & ~A >> ~B & ~B >> ~A"
#print(to_cnf(test))
#print(satisfiable(test))
player.tell("~P00")
player.tell("~B00")
player.tell("~P11")
#player.tell(("B10", False))
player.tell("~B01")
#player.tell(("B00 >> (P01 | P10) & (P01 | P10) >> B00", True))
#player.tell(("B10 >> (P00 | P11 | P20) & (P00 | P11 | P20) >> B10", True))
#player.tell(("B10", False))

board.place_object((0,0), player)
board.place_object((2,0), Pit())
board.place_object((1,2), Pit())
board.place_object((0,2), Pit())
board.place_object((4,4), Gold())
board.place_object((3,3), Pit())
board.place_object((4,0), Pit())
#board.place_object((1,0), Gold())
while(board.game_over == False):
	# for interactive
	#if(os.name is "posix"):
	#	os.system("clear")
	#else:
	#	os.system("cls")
	os.system("clear")
	print("Game Over?: " + str(board.game_over))
	print(board.getString())
	board.step()
	print("Knowledge: " + str(board.agent.kb) + "\n\n")
	print("Rule set: " + str(board.agent.rule_set))
	print("\n\nPossible Solutions: " + str(board.agent.ask("test")))
	time.sleep(1)

os.system("clear")
print("Game Over?: " + board.game_over_m)
print(board.getString())
print("Knowledge: " + str(board.agent.kb) + "\n\n")
print("Rule set: " + str(board.agent.rule_set))
print("\n\nPossible Solutions: " + str(board.agent.ask("test")))