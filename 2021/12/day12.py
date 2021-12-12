from collections import defaultdict, deque
import re
from copy import deepcopy
import math
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt
from matplotlib import colors


with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

neighbours = defaultdict(lambda : set())
for line in lines:
    dep, arr = line.split("-")
    neighbours[dep].add(arr)
    neighbours[arr].add(dep)
    

def dfs_paths(neighbours, start, goal):
    # init stack with current vertex and current path
    stack = [(start, [start])]
    # keep looping until stack is empty
    while stack:
        # remove last vertex+path from stack and store
        (vertex, path) = stack.pop()
        # go through all neighbours, with lower case neighbours, that are within the current path removed (set subtraction)
        for next in neighbours[vertex] - set([c for c in path if c.islower()]):
            # if the end is found, return/ yield the path, else add to the stack
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

print(len(list(dfs_paths(neighbours, 'start', 'end'))))

# PART 2

# SUPER INEFFICIENT AND SLOW (few min to run), but uses PART 1 code
# make new neighbours dict where always a single small cave node is duplicated and has all the same neighbours... essentially allowing to be visited twice
total_paths = []
for smallCave in [key for key in neighbours.keys() if (key.islower() and key not in ["start", "end"])]:
    newNeighbours = deepcopy(neighbours)
    newNeighbours["xtracave"] = neighbours[smallCave]
    for c in newNeighbours["xtracave"]:
        newNeighbours[c].add("xtracave")

    for path in list(dfs_paths(newNeighbours, 'start', 'end')):
        path = [c.replace('xtracave', smallCave) for c in path]
        if path not in total_paths:
            total_paths.append(path)

print(len(total_paths))

# failed attemps
'''def dfs_paths_part2(neighbours, start, goal):
    # init stack with current vertex and current path
    stack = [(start, [start], False)]

    # keep looping until stack is empty
    while stack:
        (vertex, path) = stack.pop()
        removeAllSmall = set([c for c in path if (c.islower())]) - set([c for c in path if (c.islower() and len(c) == 1 and small_visited_twice)])
        for next in neighbours[vertex] - removeAllSmall:
            if next in set([c for c in path if c.islower()]): small_visited_twice = True
            # if the end is found, return/ yield the path, else add to the stack
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))'''




'''def findPaths(stack, neighbours, paths_taken):
    for n in neighbours[stack[-1]]:
        if n == "end":
            stack.append(n)
            paths_taken.append(list(stack))
            return


        if not ((n.islower()) and (n in stack)):
            stack.append(n)
            # if path wasn't taken before, go down it
            if all(list(stack) != path[:len(stack)] for path in paths_taken):
                findPaths(stack, neighbours, paths_taken)
            else:
                # undo stack push
                stack.pop()
            
        # pop stack and try next neighbour on next iteration
        stack.pop()

    return'''



'''paths_taken = []
while True:
    stack = deque()
    stack.append('start')

    fail_count = 0
    while True:
        stack_is_updated = False
        path_found = False

        for n in neighbours[stack[-1]]:
            if n == 'end':
                stack.append(n)
                paths_taken.append(list(stack))
                path_found = True
                break

            if not ((n.islower()) and (n in stack)):
                stack.append(n)
                # if path was not taken before
                if all(list(stack) != path[:len(stack)] for path in paths_taken):
                    stack_is_updated = True
                else:
                    # undo append
                    stack.pop()
                    fail_count += 1
                    continue
        
        # go to next node if a valid one was found
        if stack_is_updated:
            continue

        # make a new stack and go again
        if path_found:
            break
        
        # if can not go to any neighbour
        break

    if fail_count == len(start)
print(paths_taken)
'''


'''paths_taken = []
stack = deque()
stack.append('start')
findPaths(stack, neighbours, paths_taken)
print(paths_taken)'''