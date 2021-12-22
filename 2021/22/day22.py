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

procedures = []
for line in lines:
    state, coords = line.split(" ")
    xrange, yrange, zrange = coords.split(",")
    
    procedure = {}
    procedure["state"] = 1 if state=='on' else 0
    procedure["x"] = list(map(int, xrange[2:].split("..")))
    procedure["y"] = list(map(int, yrange[2:].split("..")))
    procedure["z"] = list(map(int, zrange[2:].split("..")))

    # add 1 to top of the ranges to make them non-inclusive
    procedure['x'][1] += 1
    procedure['y'][1] += 1
    procedure['z'][1] += 1

    procedures.append(procedure)

cubeMap = np.zeros(shape=(101, 101, 101), dtype=int)

# coordinate transform ranges
def ctrans(ran, min):
    return [ran[0] + min, ran[1] + min]

############ PART 1 ################
for proc in procedures:
    x, y, z= proc['x'], proc['y'], proc["z"]
    
    if -50 <= x[0] and x[1] <= 50 and -50 <= y[0] and y[1] <= 50 and -50 <= z[0] and z[1] <= 50:
        
        x, y, z = ctrans(x, 50), ctrans(y, 50), ctrans(z, 50)

        cubeMap[x[0]:x[1], y[0]:y[1], z[0]:z[1]] = proc['state']

print(np.count_nonzero(cubeMap))

############ PART 2 ################

# IDEA
'''
keep an array of Cube objects where each one represents a cube of 'on' states.
If an "off" cube is added we split every cube it intersects into smaller cubes
of on states
'''

def overlap1D(range1, range2):
    if range1[1] > range2[1]:
        if range2[1] >= range1[0]:
            return True
    if range2[1] > range1[1]:
        if range1[1] >= range2[1]:
            return True
    if range1[1] == range2[1]: return True
    return False

# if there is a overlap then there must be at least 1 shared point in each of the x,y and z ranges
def overlap3D(cube1, cube2):
    if overlap1D(cube1['x'], cube2['x']):
        if overlap1D(cube1['y'], cube2['y']):
            if overlap1D(cube1['z'], cube2['z']):
                    return True
    return False

# splits cube into two cubes. The cut is made along the plane defined by the axis pair
# and at a distance distPerpAxis along the axis perpendicular to the plane defined by axis Pair
def cutCube(cube, distPerpAxis, axisPair):
    perpAxis = (set('x', 'y', 'z') - set(axisPair))[0]

    cRange = cube[perpAxis]
    cube1, cube2 = deepcopy(cube), deepcopy(cube)
    cube1[perpAxis] = [cRange[0], min([distPerpAxis, cRange[1]])] 
    cube2[perpAxis] = [max([distPerpAxis, cRange[0]]), cRange[1]] 

    # add new cubes to newcube list
    newCubes = []
    for newCube in [cube1, cube2]:
        if newCube.values() != cube.values():
            newCubes.append(newCube)

    # if no new cubes crated just add old cube to list
    if not newCubes:
        newCubes.append(cube)
    
    return newCubes


# slices cube into smaller cubes and leaves a gap that fits the slicerCube
# returns list of smaller cubes (max 26 cubes)
def subCube(cube, slicerCube):
    pass
    # we make 6 cuts of 'cube'. One cut along each of the 6 faces of the 'slicer'cube

    #cutCube(cube, distPerpAxis=, axisPair=)


cubes = []

for proc in procedures:

    if proc['state'] == 1: 
        newCube = {'x': proc['x'], 'y': proc['y'], 'z': proc['z']}
        # find other cubes that overlap with new one
        for cube in cubes:
            if overlap3D(newCube, cube):
                # for each cube that overlaps the new one, we slice it into smaller cubes but leave a hole where the new one goes (max 26 new cubes)
                sub(cube, newCube)

