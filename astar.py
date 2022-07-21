import time
# from datetime import datetime


class Node:
    # A node class to represent a point in pathfinding

    # Default constructor for class, takes optional parent Node and position(tuple) as parameters
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    # Equality definition to compare Node positions
    def __eq__(self, other):
        return self.position == other.position


# Function returns a list of tuples as a path from start node to the end node in the puzzle
# the tuples are x,y coordinates in the two-dimensional list (puzzle)
def astar_algo(puzzle, start, end):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0  # assign 0 to f,h and g properties
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0  # assign 0 to f,h and g properties

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node to open list
    open_list.append(start_node)

    # Loop until there are no more nodes in the open list
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]  # get the node on top of the open list queue
        current_index = 0
        for index, item in enumerate(open_list):  # go through list till node with smallest f value is current
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # remove current node from open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # If the end node has been found i.e. current node is the end node, get path and return
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:  # go through parent nodes and add to path
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path (from start to end)

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range i.e. if it's out of the puzzle's dimensions, skip this position
            if node_position[0] > (len(puzzle) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(puzzle[len(puzzle) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain (it's not an obstacle). In the puzzle if it's not a 0 then it's an obstacle
            if puzzle[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # add new node to children list
            children.append(new_node)

        # Loop through children and calculate their g,h and f values
        for child in children:

            # If child is in the closed list, skip it
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list and new g value is greater than existing, skip it
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


# Function to test the algorithm
def run_algo():
    # A two-dimensional list representing a puzzle/maze with x,y coordinates
    # e.g. in this view, the coordinate (1,2) represents the point at the second row and third column
    # the 1's are obstacles, so any search must by-pass them
    puzzle = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)  # the start point in this example (you can change, as long as it's in range of puzzle above)
    end = (7, 6)  # the end point in this example (you can also change, as long as it's in range of puzzle above)
    start_time = time.time()  # Get time before calling function
    path = astar_algo(puzzle, start, end)  # returns the path from the start node to the end node (in x,y coordinates)
    end_time = time.time()  # Get time after calling function

    print("Path from start to end: ", path)  # prints the path out to the console
    print("Time of execution: ", float(end_time-start_time))


# Always true when not imported module
if __name__ == '__main__':
    run_algo()
