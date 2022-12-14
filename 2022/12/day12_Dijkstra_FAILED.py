from string import ascii_lowercase
import numpy as np
from collections import deque, defaultdict

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

# builds path from list of previous nodes
def build_path(prev, current):
    path = [current]
    while current in prev.keys():
        current = prev[current]
        path.append(current)
    return path[::-1]

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
dist = np.zeros(shape=hMap.shape)
prev = defaultdict(lambda: None)
Q = deque() 
for i in range(len(hMap)):
    for j in range(len(hMap[0])):
        pos = (i, j)

        dist[pos] = np.infty
        Q.append(pos)

dist[start] = 0

while len(Q) != 0:
    # find vertex u with current shortest path
    u = None
    mindist = np.infty
    for x in Q:
        if dist[x] < mindist:
            u = x
            mindist = dist[x]
    
    if u == None:
        break

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

        # max height difference going up is 1
        if hMap[neighbour] - hMap[u] > 1: continue

        alt = dist[u] + 1
        if alt < dist[neighbour]:
            dist[neighbour] = alt
            prev[neighbour] = u


print(dist)

path = build_path(prev, end)

stepmap = np.zeros(shape=hMap.shape, dtype=int)
for i, p in enumerate(path):
    stepmap[p] = i

print(stepmap)