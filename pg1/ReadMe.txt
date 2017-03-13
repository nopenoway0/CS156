This program has been seperated into 4 different python files. To run, use:
	python pg1.py
this file contains the main method that will start the program
It will print the robot as it traverses the environment at 1 second intervals. Then it will print out a fraction of how many rooms were cleaned - this is the performance metric.

To create a custom environment run:
	python custom.py
see Creating a custom environment for more details

IF the program is too slow, on line 34 in pg1.py, replace the number 1 with 0 and each run will be instantaneous

environment.py contains things pertaining the environment. This includes both the Room class, an object that is passable and can be cleaned, and the Environment class. The Environment class is a container for objects, such as robots or Rooms. In addition, it must be passed a metric function.

interfaces.py contains all necessary abstract classes. These consist of the Object, Metric, and Agent classes. See file for details.

pg1_robot.py contains the reflex agent.

pg1.py contains the main method. Here the rooms can be modified, in size or order, to try different configurations

**********************************************************************************************************************************************************
Performance scores - for the default configuration
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

**********************************************************************************************************************************************************
Creating a custom environment
**********************************************************************************************************************************************************
1.) After running python custom.py, it will prompt you to enter the dimensions of the environment. This affects the maximum amount of rooms you can add.
2.) After entering the maximum amount of rooms, it will print out how your environment currently looks. "." means empty space, there is no object currently present.
3.) The next step is to begin constructing your environment. Keeping your coordinates within the bounds of your environment, you can begin to alter rooms.
	a.)For example, lets say you have constructed 3x3 environment. The grid is represented as follows: 
		(0,0) (1,0) (2,0)
		(0,1) (1,1) (2,1)
		(0,2) (1,2) (2,2)
	b.) Thus if you would like to change the center you would enter 1 at the first prompt and 1 at the second prompt.
	c.) You will then be asked if the room should be dirty or clean - 1 changes to room to clean, and 0 changes it to dirty
	d.) To continue modifying the room, you may enter y or 1 at the next prompt, any other request will end the changing sequence
	e.) The prompt that follows indicates the time it takes in between frames. This must be a natural number. For example, 1 - the recommended input, means it will take 1 second in between moves.
	f.) You will then be prompted to enter the coordinates of where to place the robot. This is done in the same way as the room.
	g.) once this is entered the simulation will begin

Warnings - the robot must be placed within a valid room. A room must not be placed outside the space of the environment.