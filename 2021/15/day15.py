from collections import defaultdict, deque
import re
from copy import deepcopy
import math
import heapq
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt


# heuristic function that returns estimate for distance from node a to node b
def h(rMap, a, b):
    i = abs(b[0] - a[0])
    j = abs(b[1] - a[1])

    # ideally i+j steps will need to be made, and each step has 5 risk on average
    return 5 * (i + j)

# builds path from list of previous nodes
def build_path(prev, current):
    path = [current]
    while current in prev.keys():
        current = prev[current]
        path.append(current)
    return path[::-1]

# A* pathfinding alg
def A_Star(rMap, start, target, h):

    # priority Q implemented with heapq
    Q = [start]
    heapq.heapify(Q)

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    prev = defaultdict(lambda: None)

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = defaultdict(lambda: np.inf)
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    fScore = defaultdict(lambda: np.inf)
    fScore[start] = h(rMap, start, target)

    while Q:
        # get node with lowest fScore[n] and removes it from Q
        u = heapq.heappop(Q)

        if u == target:
            return build_path(prev, u)

        # create list of neighbours
        neighbours = []
        if 0 <= u[0]-1 < len(rMap): neighbours.append((u[0]-1, u[1]))
        if 0 <= u[0]+1 < len(rMap): neighbours.append((u[0]+1, u[1]))

        if 0 <= u[1]-1 < len(rMap[0]): neighbours.append((u[0], u[1]-1))
        if 0 <= u[1]+1 < len(rMap[0]): neighbours.append((u[0], u[1]+1))

        for v in neighbours:
            # rMap[v] is the weight of the edge from u to v
            # tentative_gScore is the distance from start to v through u
            tentative_gScore = gScore[u] + rMap[v]
            if tentative_gScore < gScore[v]:
                # This path to v is better than any previous one. Record it!
                prev[v] = u
                gScore[v] = tentative_gScore
                fScore[v] = tentative_gScore + h(rMap, v, target)
                if v not in Q:
                    heapq.heappush(Q,v)
    
    # Q is empty but end not reached, return failure
    return []


##################################### Read Input File ####################################
with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]


rMap = np.zeros(shape=(len(lines), len(lines[0])), dtype=int)

for i,line in enumerate(lines):
    for j,c in enumerate(line):
        rMap[i,j] = int(c)

######################################### PART 1 #########################################
start = (0,0)
target = (len(rMap)-1, len(rMap[0])-1)

path = A_Star(rMap, start, target, h)
print(sum([rMap[coord] for coord in path[1:]]))
######################################### PART 2 #########################################
# init new bigger map
bigRMap = rMap

# expand map in j direction
for i in range(1,5):
    bigRMap = np.concatenate((bigRMap, (rMap + i - 1)%9 + 1), axis=1)

bigRRow = bigRMap
# expand map in i direction
for i in range(1,5):
    bigRMap = np.concatenate((bigRMap, (bigRRow + i - 1)%9 + 1), axis=0)

start = (0,0)
target = (len(bigRMap)-1, len(bigRMap[0])-1)

path = A_Star(bigRMap, start, target, h)
print(sum([bigRMap[coord] for coord in path[1:]]))



############################## PLOTTING JUST FOR FUN #####################################

plt.plot([c[1] for c in path],[c[0] for c in path], color='black')
plt.gca().invert_yaxis()
plt.show()







''' ORIGINAL PART 1 ANSWER

ef Dijkstra(rMap, start, target):

    Q = deque()

    dist = defaultdict(lambda: np.inf)
    prev = defaultdict(lambda: None)

    for i in range(len(rMap)):
        for j in range(len(rMap[0])):
            dist[(i,j)] # sets to inf
            prev[(i,j)] # sets to None
            Q.append((i,j))
    dist[start] = 0

    while Q:
        # get u, the closest node and remove it from Q 

        u = min(Q, key=lambda x: dist[x])
        Q.remove(u)

        # loop through neighbours v of u still in Q
        neighbours = []
        #if 0 <= u[0]-1 < len(rMap): neighbours.append((u[0]-1, u[1]))
        if 0 <= u[0]+1 < len(rMap): neighbours.append((u[0]+1, u[1]))

        #if 0 <= u[1]-1 < len(rMap[0]): neighbours.append((u[0], u[1]-1))
        if 0 <= u[1]+1 < len(rMap[0]): neighbours.append((u[0], u[1]+1))

        if u == target:
            return dist, prev

        for v in neighbours:
            # rMap[v] == length(u, v)
            alt = dist[u] + rMap[v]

            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    return dist, prev


start = (0,0)
target = (len(rMap)-1, len(rMap[0])-1)
dist, prev = Dijkstra(rMap, start, target)

path = []
u = target
if prev[u] is not None or u == start:
    while u is not None:
        path.append(u)
        u = prev[u]

path = path[::-1]

totalRisk = 0
for coord in path[1:]:
    totalRisk += rMap[coord]

print(totalRisk)

'''