import sys
from environment import Environment
from environment import Room
from pg1_robot import Robot
env_dimensions = []

env_dimensions.append(raw_input("Enter x dimension of environment space: "))
env_dimensions.append(raw_input("Enter y dimension of environment space: "))

print("Created " + str(env_dimensions[0]) + "x" + str(env_dimensions[1]) + " environment\n")

env = Environment()
env.initialize_env(int(env_dimensions[0]), int(env_dimensions[1]), Room)

print(". are empty spaces X are dirty rooms and O are clean rooms\n\n" + env.toString())

while(True):
	x = int(raw_input("Enter x coordinate of room to change: "))
	y = int(raw_input("Enter y coordinate of room to change: "))

	inp = int(raw_input("Make room dirty(0) or clean(1): "))
	dirty_or_clean = None

	if(inp == 0):
		dirty_or_clean = False
	else:
		dirty_or_clean = True

	env.getObject(x, y).set_condition(dirty_or_clean)
	env.changeObjectState(x, y, True)

	print(env.toString())

	keep_going = raw_input("Continue modifying? y/n (1/0): ")
	if(keep_going != "y" and keep_going != "1"):
		break

env.alterData(env.getNumDirtyRooms())
print("Let's place the agent. Notice, the agent must be placed on a valid room - no . ")

delay = int(raw_input("Enter delay of print messages(0 means instantaneous - 1 means 1 seconds etc.): "))

rb = Robot(delay)
x = int(raw_input("Enter x coordinate of robot: "))
y = int(raw_input("Enter y coordinate of robot: "))
env.placeObject(x, y, rb)

print("Robot placed\n" + env.toString())

print("Creating metric function")

env.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

env.stageEnv()