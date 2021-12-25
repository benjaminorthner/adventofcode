from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt


with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

cMap = np.array([[char for char in line] for line in lines], dtype=str)
width = len(cMap[0])
height = len(cMap)

def step(cMapIn, dir='east'):
    cMap = deepcopy(cMapIn)
    nothingmovedEast = True
    nothingmovedSouth = True
    for r in range(height):
        for c in range(width):

            curr = cMapIn[r, c]

            if dir == 'east':
                east = cMapIn[r, (c+1) % width]
                if curr == '>' and east == '.':
                    cMap[r, c] = '.' 
                    cMap[r, (c+1) % width] = '>'
                    nothingmovedEast = False

            elif dir == 'south':
                south = cMapIn[(r+1) % height, c]
                if curr == 'v' and south == '.':
                    cMap[r, c] = '.'
                    cMap[(r+1) % height, c] = 'v'
                    nothingmovedSouth = False

    # move south
    if dir == 'east': 
        cMap, nothingmovedSouth = step(cMap, dir='south')

    return cMap, nothingmovedEast and nothingmovedSouth

def printMap(cMap):
    for row in cMap:
        for c in row:
            if c is not ".": print(c, end="")
            else: print(" ", end="")
        print("")

nothingmoved = False
count = 0
while not nothingmoved:
    cMap, nothingmoved = step(cMap)
    count += 1

printMap(cMap)
print(count)


# plot (could animate)
toint = {"." : 0, '>' : 1, 'v' : 2}
image = [[toint[c] for c in row] for row in cMap]

plt.imshow(image, cmap='magma')
plt.axis("off")
plt.show()