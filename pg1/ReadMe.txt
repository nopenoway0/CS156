This program has been seperated into 4 different python files. To run, use:
	python pg1.py
this file contains the main method that will start the program

environment.py contains things pertaining the environment. This includes both the Room class, an object that is passable and can be cleaned, and the Environment class. The Environment class is a container for objects, such as robots or Rooms. In addition, it must be passed a metric function.

interfaces.py contains all necessary abstract classes. These consist of the Object, Metric, and Agent classes. See file for details.

pg1_robot.py contains the reflex agent.

pg1.py contains the main method. Here the rooms can be modified, in size or order, to try different configurations