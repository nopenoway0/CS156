from ie1_astar import AStar, AStarNode
from math import sqrt

class AStarGrid(AStar):
    def heuristic(self, node, start, end):
        # node = your current position in the grid
        # start = the start location
        # end = the goal state location
        #
        # Implement the code for your A* heuristic here. 
        # First step is to design and ddefine the function, on paper.
        # Then implement the code to calculate the distance from
        # node to the the end goal. The start node is provided just in 
        # case you feel you want or need to use it. If ot, then just
        # ignore it.  The variables node, start, and end are instances of 
        # class AStarGridNode (see below).  To get the x position of node, 
        # for instance, just use  node.x  To get its y position, just use node.y
        #  Ditto for start nd end. 
        # After calculating the heusistic numerical distance from node to goal, return 
        # that value in the following return statement. 
        x_diff = end.x - node.x
        y_diff = end.y - node.y
        print(sqrt(x_diff*x_diff + y_diff*y_diff))
        return sqrt(x_diff*x_diff + y_diff*y_diff)

        # return your calculated heusistic numerical distance here

class AStarGridNode(AStarNode):
    def __init__(self, x, y):
        self.x, self.y = x, y
        super(AStarGridNode, self).__init__()

    def move_cost(self, other):
        # other is an AStarGridNode  type object
        #
        # This member function computes the A*  "g"  cost of going from 
        # the current node (i.e., self) to the other node. It returns a
        # numeric value that is the the distabnce from "self" to "other" 
        # Then return that calculated value. 
        
        return self.g +  other.g

        # return the calculated distance from self (current node) to other node

    def __repr__(self):
        return '(%d %d)' % (self.x, self.y)
