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
player.tell("~B01 >> ~(P11 | P02)")
player.tell("~P00")
player.tell("~B00")
player.tell("~B01")
player.tell("~P01")
#player.tell(("B00 >> (P01 | P10) & (P01 | P10) >> B00", True))
#player.tell(("B10 >> (P00 | P11 | P20) & (P00 | P11 | P20) >> B10", True))
start_location = (0,0)
board.place_object(start_location, player)
board.place_object((3,0), Pit())
board.place_object((4,4), Gold())
board.place_object((3,3), Pit())
board.place_object((0,4), Pit())
board.place_object((2,1), Pit())
board.place_object((1,2), Pit())
#board.place_object((1,0), Gold())
while(board.game_over == False):
	# for interactive
	#if(os.name is "posix"):
	#	os.system("clear")
	#else:
	#	os.system("cls")
	os.system("clear")
	print("Game Over?: " + str(board.game_over))
	print("Orientation: " + str(player.orientation))
	print("Current Location: " + str((player.x, player.y)))
	print(board.getString())
	print("Knowledge: " + str(board.agent.kb) + "\n\n")
	print("Rule set: " + str(board.agent.rule_set))
	#print("\n\nPossible Solutions: " + str(board.agent.ask("test")))
	#time.sleep(0.1)
	board.step()
	time.sleep(0.5)
	if(board.game_over_m == "You died!"):
		board.game_over_m = ""
		board.game_over = False
		player.changeOrientation((1,0))
		board.place_object(start_location, player)

os.system("clear")
print("Game Over?: " + board.game_over_m)
print(board.getString())
print("Found the following pits: " + str(board.agent.pits) + "\n\n")
print("Rule set: " + str(board.agent.rule_set))