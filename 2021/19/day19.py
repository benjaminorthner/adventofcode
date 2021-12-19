from collections import defaultdict, deque
import regex
from copy import deepcopy
import math
import sys
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt
from matplotlib import colors

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]


scanners = []

for i, line in enumerate(lines):

    if line[0:3] == "---":
        scanner = defaultdict(lambda:[])
        scanner['id'] = regex.findall(r"\d+", line)[0]
           

    elif line is not "":
        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)
        scanner['relBeaconCoords'].append(np.array([x,y,z]))
        # start of with abs and rel coords being the same
        scanner['absBeaconCoords'].append(np.array([x,y,z]))

    if line == "" or i == len(lines)-1:
        scanners.append(scanner)

def distance(coords1, coords2):
    return np.linalg.norm(coords1-coords2)

# aligns scanner2 relative to scanner1
def align(scanner1, scanner2):

    # fitScore is lower the better the alignment is
    fitScore = np.inf

    # keep aligning till manual break
    while True:
        prevFitScore = fitScore
        # for each beacon in scanner2, find the closes one in scanner1
        closestS1Beacon = []
        for S2BeaconCoord in scanner2['absBeaconCoords']:
            min = np.inf
            closestBeaconNum = -1
            for i, S1BeaconCoord in enumerate(scanner1['absBeaconCoords']):
                dist = distance(S1BeaconCoord, S2BeaconCoord)

                # check if current S1 beacon is closest
                if dist < min:
                    min = dist
                    closestBeaconNum = i

            # append both which S1 beacon is closest and how far it is
            closestS1Beacon.append([closestBeaconNum, min])

        # find the center of mass of the S1 beacons that are in the closestS1Beacon list
        COMCoordS1 = np.zeros(3)
        cnt = 0
        for S1BeaconNum in set([num[0] for num in closestS1Beacon]):
            COMCoordS1 += scanner1['absBeaconCoords'][S1BeaconNum]
            cnt += 1
        COMCoordS1 *= 1/cnt
        
        # find the center of mass of all the S2 beacons
        COMCoordS2 = np.zeros(3)
        for coord in scanner2['absBeaconCoords']:
            COMCoordS2 += coord 
        COMCoordS2 *= 1/len(scanner2['absBeaconCoords'])

        # calc translation vector for how to move scanner 2 coords for COMs to match up (must be interger)
        translationVec = np.round(COMCoordS1 - COMCoordS2).astype(int)
        print(translationVec)

        # move all absolute S2 Coords by translation Vec
        newCoords = scanner2['absBeaconCoords'] + translationVec

        # calculate fit score after alignment (mean of minimum distances)
        fitScore = np.mean([num[1] for num in closestS1Beacon])

        # if fit score is better: accept newCoords and do another alignment, else break
        if fitScore < prevFitScore: scanner2['absBeaconCoords'] = newCoords
        else: break




align(scanners[0], scanners[1])



