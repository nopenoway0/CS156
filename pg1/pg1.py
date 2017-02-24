# Python library import
import time
import sys
from math import sqrt
import copy
import os

# Custom classes import
from interfaces import Object
from pg1_robot import Robot
from interfaces import Agent
from interfaces import Object
from interfaces import Metric
from environment import Environment
from environment import Room

def init_message():
	print("**********************************\n")
	print("****** X is a dirty room *********\n")
	print("****** O is a clean room *********\n")
	print("******  R is the Robot   *********")
	print("**********************************\n")

#***********************************************MAIN METHOD*************************************************************************************************************************#
# Welcome Message
init_message()

# Create Empty Environment
env = Environment()
# Initiliaze enviornment with size and object classes
env.initialize_env(4, 4, Room)

# Create Robot Agent
rb = Robot()

env.changeObjectState(0,0, True)
env.changeObjectState(1,0, True)
#env.changeObjectState(0,1, True)
env.changeObjectState(2,0, True)
env.changeObjectState(2,1, True)
# set number of dirty rooms
env.alterData(env.getNumDirtyRooms())

# Place Robot
env.placeObject(0, 0, rb)

# Set up all metrics
env.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

# Start Simulation - output is performance metric
print(env.toString())
time.sleep(1)
performance = env.stageEnv()