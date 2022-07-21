import time
import math
import numpy as np
from random import randint


class Node:
    # A node class to represent a point in pathfinding

    # Default constructor for class, takes dimension(tuple) as parameters
    def __init__(self, dimension=None):
        self.dimension = dimension

    # Equality definition to compare Node positions
    def __eq__(self, other):
        return self.dimension == other.dimension


class Fly(Node):
    def __init__(self, dimension=None):
        super().__init__(dimension)

        self.fitness = 0  # To store a fly's fitness value
        self.prev_dimensions = []  # To keep track of a fly's previous positions


def calculate_fitness(fly, end_node):  # fly IS A VECTOR REPRESENTING ONE FLY with 2 dimensions(fly,y)
    distance = ((fly.dimension[0] - end_node.dimension[0]) ** 2) + (
            (fly.dimension[1] - end_node.dimension[1]) ** 2)
    return distance


def dfo_algo(puzzle, end_point):
    num_of_flies = 5  # POPULATION SIZE
    dimensions = 2  # DIMENSIONALITY
    delta = 0.001  # DISTURBANCE THRESHOLD
    max_iterations = 100  # ITERATIONS ALLOWED

    FLIES = []  # EMPTY FLIES ARRAY OF SIZE: (num_of_flies,dimensions)
    # fitness = []

    end_node = Node(end_point)
    lower_b = 0  # lower boundary
    upper_b = len(puzzle[len(puzzle) - 1]) - 1  # the length of the last list in this 2D puzzle is the upper boundary

    # Initialize all flies by generating random dimensions for them
    for i in range(num_of_flies):
        # generate random dimensions for this fly within puzzle bounds
        random_dimen = (randint(lower_b, (len(puzzle) - 1)), randint(lower_b, upper_b))
        fly = Fly(random_dimen)
        FLIES.append(fly)

    best_fly = FLIES[0]  # Assign first fly as best fly (a formality)
    best_fly_index = 0

    # ==================
    # Loop until max number of iterations reached or till end point is found by a fly
    for iteration in range(max_iterations):

        # Check if end point is reached by a fly and exit with fly
        # for fly in FLIES:
        #     if fly == end_node:
        #         return fly

        # Generate fitness for all flies AND find best fly ================
        for i, fly in enumerate(FLIES):  # Fitness for all flies
            fly.fitness = calculate_fitness(fly, end_node)  # calculate fitness for this fly
            # fitness.append(fly.fitness)  # add all fitness values to array
            # if i == 0: best_fly = fly  # assign first fly as best fly (formality)
            if fly.fitness < best_fly.fitness:
                best_fly = fly  # Assign best fly (the shortest distance from end point)
                best_fly_index = i  # Best fly index

        # current_best_fitness = min(fitness)
        if iteration % 10 == 0:  # PRINT BEST FLY EVERY 10 ITERATIONS (for demonstration)
            print("Iteration:", iteration, "\tBest fly dimension:", best_fly.dimension,
                  "\tBest fly index:", best_fly_index, "\tFitness value:", best_fly.fitness)

        # Going through each fly, to update, and to check if end point has been found
        for i, fly in enumerate(FLIES):
            if i == best_fly_index:
                continue  # this is the best fly, no need to update its dimensions

            # FIND BEST NEIGHBOUR
            left = (i - 1) % num_of_flies  # Left neighbour index
            right = (i + 1) % num_of_flies  # Right neighbour index
            best_neighbour_index = right if FLIES[right].fitness < FLIES[left].fitness else left  # best neighbour index
            best_neighbour = FLIES[best_neighbour_index]

            # save current dimension (for demonstration purposes; to show fly previous positions)
            fly.prev_dimensions.append(fly.dimension)

            # Because tuples do not allow item assignment,
            # the dimension is converted to a list (its reassigned as tuple)
            # fly_list is essentially a placeholder for fly.dimension
            fly_list = list(fly.dimension)

            # UPDATING dimensions============
            # First Dimension Update
            u = np.random.rand()
            if u < delta:  # If random (u) is less than disturbance value, assign new random value
                fly_list[0] = randint(lower_b, upper_b)
            else:
                # update dimension value (///ROUND UP)
                fly_list[0] = math.ceil(best_neighbour.dimension[0] + u * (best_fly.dimension[0] - fly.dimension[0]))

            # Second Dimension Update
            u = np.random.rand()
            if u < delta:  # If random (u) is less than disturbance value, assign new random value (within bounds)
                fly_list[1] = randint(lower_b, upper_b)
            else:
                # update dimension value (///ROUND UP)
                fly_list[1] = math.ceil(best_neighbour.dimension[1] + u * (best_fly.dimension[1] - fly.dimension[1]))

            # OUT OF BOUND CONTROL
            # Make sure within range i.e. if it's out of the puzzle's dimensions, generate new random dimensions
            # NOTE: This check may not be necessary as long as the generation of the random dimensions takes into
            # account the puzzle bounds
            if fly_list[0] > (len(puzzle) - 1) or fly_list[0] < 0:  # checking bounds for 1st index
                fly_list[0] = randint(lower_b, upper_b)

            if fly_list[1] > (len(puzzle[len(puzzle) - 1]) - 1) or fly_list[1] < 0:  # checking bounds for 2nd index
                fly_list[1] = randint(lower_b, upper_b)

            # Make sure walkable terrain (it's not an obstacle). In the puzzle if it's not a 0 then it's an obstacle
            # Loop until value at coordinate is not obstacle(1). Max iterations is 10, (then fly might be on obstacle)
            # remove the count breaker if you prefer (more ideal but time-consuming imo)
            count = 0
            while puzzle[fly_list[0]][fly_list[1]] != 0 or count < 10:
                fly_list[0] = randint(lower_b, upper_b)
                fly_list[1] = randint(lower_b, upper_b)
                count += 1

            fly.dimension = tuple(fly_list)  # assign updated dimensions
            if fly == end_node:
                fly.prev_dimensions.append(fly.dimension)
                return fly

    return Fly()  # return empty fly


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

    end = (7, 6)  # the end point in this example (you can also change, as long as it's in range of puzzle above)
    start_time = time.time()  # Get time before calling function
    fly = dfo_algo(puzzle, end)  # returns the fly that found the end point or an empty fly
    end_time = time.time()  # Get time after calling function

    if fly.dimension is None:
        print("Max Iterations run before any fly found end")  # If iterations run out before a fly found end
    else:
        print("Fly Dimensions from start to end: ", fly.prev_dimensions)  # prints the fly's prev's dimensions
    print("Time of execution: ", float(end_time-start_time))


# Always true when not an imported module
if __name__ == '__main__':
    run_algo()
