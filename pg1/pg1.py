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
rb = Robot(1)

# Intialiaze environment space by enabling rooms. Disabled rooms act as walls
# Coordinates layout is as follows:
# (0,0) (1,0) (2,0)
# (0,1) (1,1) (2,1)
# (0,2) (1,2) (2,2)
# etc.
env.changeObjectState(0,0, True)
env.changeObjectState(1,0, True)
env.changeObjectState(2,0, True)

# set number of dirty rooms as data to be compared with the metric
env.alterData(env.getNumDirtyRooms())

# Place Robot
env.placeObject(0, 0, rb)

# Set up all metrics by passing in metric function, initialization function and calculation function as specified by Metric interface in interfaces.py
# XXX
env.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

# Inital print of environemnt
print("Config: XXX")
print(env.toString())
time.sleep(1)

# Start simulation
performance = env.stageEnv()

# Intialize and Start second Simlution
# X0X
print("Config: XOX")
rb.reset()
env2 = Environment()
env2.initialize_env(4,4, Room)
env2.changeObjectState(0,0, True)
env2.getObject(1,0).set_condition(True)
env2.changeObjectState(1,0, True)
env2.changeObjectState(2,0, True)
env2.placeObject(0, 0, rb)
env2.alterData(env2.getNumDirtyRooms())
env2.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

print(env2.toString())
time.sleep(1)
performance = env2.stageEnv()

# 0XX
print("Config: OXX")
rb.reset()
env3 = Environment()
env3.initialize_env(4,4, Room)
env3.getObject(0,0).set_condition(True)
env3.changeObjectState(0,0, True)
env3.changeObjectState(1,0, True)
env3.changeObjectState(2,0, True)
env3.placeObject(0, 0, rb)
env3.alterData(env3.getNumDirtyRooms())
env3.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

print(env3.toString())
time.sleep(1)
performance = env3.stageEnv()

# 00X
print("Config: OOX")
rb.reset()
env4 = Environment()
env4.initialize_env(4,4, Room)
env4.getObject(0,0).set_condition(True)
env4.getObject(1,0).set_condition(True)
env4.changeObjectState(0,0, True)
env4.changeObjectState(1,0, True)
env4.changeObjectState(2,0, True)
env4.placeObject(0, 0, rb)
env4.alterData(env4.getNumDirtyRooms())
env4.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

print(env4.toString())
time.sleep(1)
performance = env4.stageEnv()

# XX0
print("Config: XXO")
rb.reset()
env5 = Environment()
env5.initialize_env(4,4, Room)
env5.getObject(2,0).set_condition(True)
env5.changeObjectState(0,0, True)
env5.changeObjectState(1,0, True)
env5.changeObjectState(2,0, True)
env5.placeObject(0, 0, rb)
env5.alterData(env5.getNumDirtyRooms())
env5.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

print(env5.toString())
time.sleep(1)
performance = env5.stageEnv()

# 000
print("Config: OOO")
rb.reset()
env6 = Environment()
env6.initialize_env(4,4, Room)
env6.getObject(2,0).set_condition(True)
env6.getObject(1,0).set_condition(True)
env6.getObject(0,0).set_condition(True)
env6.changeObjectState(0,0, True)
env6.changeObjectState(1,0, True)
env6.changeObjectState(2,0, True)
env6.placeObject(0, 0, rb)
env6.alterData(env6.getNumDirtyRooms())
env6.initialize_metric(Robot.metric_func, Robot.init_metric, Robot.calc_metric)

print(env6.toString())
time.sleep(1)
performance = env6.stageEnv()

