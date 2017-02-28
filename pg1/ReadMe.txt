This program has been seperated into 4 different python files. To run, use:
	python pg1.py
this file contains the main method that will start the program
It will print the robot as it traverses the environment at 1 second intervals. Then it will print out a fraction of how many rooms were cleaned - this is the performance metric.

IF the program is too slow, on line 34 in pg1.py, replace the number 1 with 0 and each run will be instantaneous

environment.py contains things pertaining the environment. This includes both the Room class, an object that is passable and can be cleaned, and the Environment class. The Environment class is a container for objects, such as robots or Rooms. In addition, it must be passed a metric function.

interfaces.py contains all necessary abstract classes. These consist of the Object, Metric, and Agent classes. See file for details.

pg1_robot.py contains the reflex agent.

pg1.py contains the main method. Here the rooms can be modified, in size or order, to try different configurations

**********************************************************************************************************************************************************
Performance scores
**********************************************************************************************************************************************************

The robot was tested with the following configurations(X is a dirty room, O is a clean room) - the robot always starts in the left corner of the rooms:

XXX

Cleans All 3 rooms

OXX

Cleans 2 Rooms

OOX

Cleans no Rooms


X0X

Cleans 0 rooms

X00

Cleans 1 Room

000

Cleans no Room