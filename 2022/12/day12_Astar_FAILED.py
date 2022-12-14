from collections import defaultdict
import heapq
import numpy as np
from string import ascii_lowercase


# heuristic function that returns estimate for distance from node a to node b
def h(a, b):
    i = abs(b[0] - a[0])
    j = abs(b[1] - a[1])

    # ideally i+j steps will need to be made
    return i + j

# builds path from list of previous nodes
def build_path(prev, current):
    path = [current]
    while current in prev.keys():
        current = prev[current]
        path.append(current)
    return path[::-1]

# A* pathfinding alg
def A_Star(hMap, start, target, h):
    # priority Q implemented with heapq
    Q = [start]
    heapq.heapify(Q)

    # For node n, prev[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    prev = defaultdict(lambda: None)

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = defaultdict(lambda: np.inf)
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    fScore = defaultdict(lambda: np.inf)
    fScore[start] = h(start, target)

    while Q:
        # get node with lowest fScore[n] and removes it from Q
        u = heapq.heappop(Q)

        if u == target:
            return build_path(prev, u)

        # create list of neighbours
        neighbours = []
        if 0 <= u[0]-1 < len(hMap): neighbours.append((u[0]-1, u[1]))
        if 0 <= u[0]+1 < len(hMap): neighbours.append((u[0]+1, u[1]))

        if 0 <= u[1]-1 < len(hMap[0]): neighbours.append((u[0], u[1]-1))
        if 0 <= u[1]+1 < len(hMap[0]): neighbours.append((u[0], u[1]+1))

        for v in neighbours:

            # height difference is max 1
            if abs(hMap[v] - hMap[u]) > 1: continue

            # hMap[v] is the weight of the edge from u to v
            # tentative_gScore is the distance from start to v through u
            tentative_gScore = gScore[u] + hMap[v]
            if tentative_gScore < gScore[v]:
                # This path to v is better than any previous one. Record it!
                prev[v] = u
                gScore[v] = tentative_gScore
                fScore[v] = tentative_gScore + h(v, target)
                if v not in Q:
                    heapq.heappush(Q,v)
    
    # Q is empty but end not reached, return failure
    return []

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

# make map find start and end
hMap = np.array([list(line) for line in lines])
start = (np.where(hMap == "S")[0][0], np.where(hMap == "S")[1][0])
end = (np.where(hMap == "E")[0][0], np.where(hMap == "E")[1][0])

# replace start with a and end with z
hMap[start] = 'a'
hMap[end] = 'z'

# convert height map from letters to integers
hMap = np.vectorize(ascii_lowercase.index)(hMap)


path = A_Star(hMap, end, start, h)
print(len(path))

stepmap = np.zeros(shape=hMap.shape, dtype=int)
for i, p in enumerate(path):
    stepmap[p] = i

print(stepmap)

"""
from string import ascii_lowercase
import numpy as np
from collections import deque

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

# make map find start and end
hMap = np.array([list(line) for line in lines])
start = (np.where(hMap == "S")[0][0], np.where(hMap == "S")[1][0])
end = (np.where(hMap == "E")[0][0], np.where(hMap == "E")[1][0])

# replace start with a and end with z
hMap[start] = 'a'
hMap[end] = 'z'

# convert height map from letters to integers
hMap = np.vectorize(ascii_lowercase.index)(hMap)

# Dijkstra
dist = np.zeros(shape=hMap.shape, dtype=int)
prev = np.zeros(shape=hMap.shape, dtype=int)
Q = deque() 
for i in range(len(hMap)):
    for j in range(len(hMap[0])):
        pos = (i, j)

        dist[pos] = 100000000000000
        Q.append(pos)

dist[start] = 0

while len(Q) != 0:
    # find vertex u with current shortest path
    u = None
    mindist = 1000000000000000
    for x in Q:
        if dist[x] < mindist:
            u = x
            mindist = dist[x]
    
    # remove it from the queue
    Q.remove(u)

    # can end here if we reach the end of the code
    if u == end:
        break

    # loop over neighbours of u
    for shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

        neighbour = (u[0] + shift[0], u[1] + shift[1])
        
        # neighbour must still be in queue
        if neighbour not in Q: continue

        # height difference is max 1
        if abs(hMap[neighbour] - hMap[u]) > 1: continue

        alt = dist[u] + 1
        if alt < dist[neighbour]:
            dist[neighbour] = alt
            #prev[neighbour] = u


print(dist[end])
"""