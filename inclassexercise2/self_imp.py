from sympy import *
import os
from explorer import Explorer, Agent
from environment import Environment, Pit, Gold, Wumpus
import time

##### Main #####

board = Environment()
player = Explorer()

player.tell("~B01 >> ~(P11 | P02)")
player.tell("~P00")
player.tell("~B00")
player.tell("~B01")
player.tell("~P01")

start_location = (0,0)
board.place_object(start_location, player)
board.place_object((3,0), Pit())
board.place_object((4,4), Gold())
board.place_object((3,3), Pit())
board.place_object((0,4), Pit())
board.place_object((2,1), Pit())
board.place_object((1,2), Wumpus())

while(board.game_over == False):
	if(os.name is "posix"):
		os.system("clear")
	else:
		os.system("cls")
	print("Game Over?: " + str(board.game_over))
	print("Orientation: " + str(player.orientation))
	print("Current Location: " + str((player.x, player.y)))
	print(board.getString())
	print("Knowledge: " + str(board.agent.kb) + "\n\n")
	print("Rule set: " + str(board.agent.rule_set))
	board.step()
	time.sleep(1)
	if(board.game_over_m == "You died!"):
		board.game_over_m = ""
		board.game_over = False
		player.changeOrientation((1,0))
		board.place_object(start_location, player)

if(os.name is "posix"):
	os.system("clear")
else:
	os.system("cls")
print("Game Over?: " + board.game_over_m)
print(board.getString())
print("Found the dangers at: " + str(board.agent.pits) + "\n\n")
print("Rule set: " + str(board.agent.rule_set))