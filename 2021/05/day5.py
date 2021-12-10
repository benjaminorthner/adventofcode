import re
import numpy as np
import math

def checkVertHorz(x1,y1,x2,y2):
    if x1 == x2:
        return True
    
    if y1 == y2:
        return True

    
with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

Lines = []
for line in lines:
    coords = {}
    x1y1, x2y2 = line.split(" -> ")
    coords['x1'], coords['y1'] = x1y1.split(",")
    coords['x2'], coords['y2'] = x2y2.split(",")

    coords['x1'] = int(coords['x1'])
    coords['y1'] = int(coords['y1'])
    coords['x2'] = int(coords['x2'])
    coords['y2'] = int(coords['y2'])
    Lines.append(coords)


maxX = max([max([coords['x1'] for coords in Lines]), max([coords['x2'] for coords in Lines])]) + 1
maxY = max([max([coords['y1'] for coords in Lines]), max([coords['y2'] for coords in Lines])]) + 1

Grid = np.zeros((maxX,maxY), dtype=int)

for coords in Lines:
    if checkVertHorz(coords['x1'],coords['y1'],coords['x2'],coords['y2']):
        if coords['x1'] == coords['x2']:
            if coords['y1'] > coords['y2']:
                for y in range(coords['y1'], coords['y2']-1, -1):
                    Grid[coords['x1'], y] += 1
            else:
                for y in range(coords['y1'], coords['y2']+1):
                    Grid[coords['x1'], y] += 1
        
        if coords['y1'] == coords['y2']:

            if coords['x1'] > coords['x2']:
                for x in range(coords['x1'], coords['x2']-1, -1):
                    Grid[x, coords['y1']] += 1
            else:
                for x in range(coords['x1'], coords['x2']+1):
                    Grid[x, coords['y1']] += 1
            

p1 = 0
for x in range(maxX):
    for y in range(maxY):
        if Grid[x, y] not in [0, 1]:
            p1 += 1

print(p1)


# PART 2


def checkVertHorzDiag(x1,y1,x2,y2):
    if x1 == x2:
        return "v"
    
    if y1 == y2:
        return "h"

    if float(y2-y1) / float(x2-x1) in [1, -1]:
        return "d"


Grid = np.zeros((maxX,maxY), dtype=int)

for coords in Lines:
    
    if checkVertHorzDiag(coords['x1'],coords['y1'],coords['x2'],coords['y2']) == 'v':

        if coords['y1'] > coords['y2']:
            for y in range(coords['y1'], coords['y2']-1, -1):
                Grid[coords['x1'], y] += 1
        else:
            for y in range(coords['y1'], coords['y2']+1):
                Grid[coords['x1'], y] += 1

    elif checkVertHorzDiag(coords['x1'],coords['y1'],coords['x2'],coords['y2']) == 'h':
        if coords['x1'] > coords['x2']:
            for x in range(coords['x1'], coords['x2']-1, -1):
                Grid[x, coords['y1']] += 1
        else:
            for x in range(coords['x1'], coords['x2']+1):
                Grid[x, coords['y1']] += 1
    
    elif checkVertHorzDiag(coords['x1'],coords['y1'],coords['x2'],coords['y2']) == 'd':
        
        if coords['x1'] < coords['x2']:
            xCoords = list(range(coords['x1'], coords['x2'] + 1))
        else:
            xCoords = list(range(coords['x1'], coords['x2'] -1, -1))

        if coords['y1'] < coords['y2']:
            yCoords = list(range(coords['y1'], coords['y2']+1))
        else:
            yCoords = list(range(coords['y1'], coords['y2']-1, -1))


        for x,y in zip(xCoords, yCoords):
            Grid[x,y] += 1


p2 = 0
for x in range(maxX):
    for y in range(maxY):
        if Grid[x, y] not in [0, 1]:
            p2 += 1

print(p2)