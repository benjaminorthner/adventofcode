from collections import deque
import numpy as np
from string import ascii_lowercase


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

def bfs(part):

    # append start + distance from start (=0)
    Q = deque()
    if part == 1:
        Q.append((start, 0))
    else:
        for x in range(len(hMap)):
            for y in range(len(hMap[0])):
                if hMap[(x, y)] == 0:
                    Q.append(((x, y), 0))


    # set to track previously visited
    S = set()
    while Q:
        (x, y), d = Q.popleft()
        if (x, y) in S:
            continue
        S.add((x, y))

        # if end is reached return distance
        if (x, y) == end:
            return d
        
        # add valid neighbours to queue
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            newX = x + dx
            newY = y + dy

            # check if height difference is 1 and if within the map
            if 0 <= newX < len(hMap) and 0 <= newY < len(hMap[0]) and hMap[(newX, newY)] - hMap[(x, y)] <= 1:
                Q.append(((newX, newY), d + 1))

print(bfs(1))
print(bfs(2))
