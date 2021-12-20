from collections import defaultdict, deque
import regex
from copy import deepcopy
import math
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

# generate a list of all 24 possible 3D, 90° rotation matrices
# https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
rotationMatrices = []
A = np.array([[1, 0, 0],
              [0, 0, -1],
              [0, 1, 0]], dtype=int)
B = np.array([[0, 0, 1],
              [0, 1, 0],
              [-1, 0, 0]], dtype=int)

for p in range(0, 4):
    for q in range(0, 4):
        for r in range(0, 4):
            for s in range(0, 4):
                a = np.linalg.matrix_power(A, p)
                b = np.linalg.matrix_power(B, q)
                c = np.linalg.matrix_power(A, r)
                d = np.linalg.matrix_power(B, s)
                res = np.matmul(a, np.matmul(b ,np.matmul(c, d)))
                
                # add res if not already in list
                new = True
                for mat in rotationMatrices:
                    if (res == mat).all():
                        new = False
                if new:
                    rotationMatrices.append(res)

def rotateVec(vec, rotNumber):
    return rotationMatrices[rotNumber].dot(vec)

def distance(coords1, coords2):
    return np.linalg.norm(coords1-coords2)

# aligns scanner2 relative to scanner1
def ICPalign(scanner1, scanner2Original):
    # IDEA:
    # FIRST FIND ALL GROUPS IN SCANNER 2 OF BEACONS THAT ARE CLOSE TOGETHER (groups of three)
    # THEN CALCULATE SOME SORT OF ROTATIONALLY INVARIANT NUMBER FOR EACH GROUP.
    # THEN FIND THE GROUPS IN SCANNER 1 AND ALSO CALC THAT NUMBER. 
    # MARK ALL THE GROUPS IN SCANNER 2 WITH THE MATCHING INVARIANT IN SCANNER 1 AS GOOD
    # PERFORM THE ICP WHERE THE SCANNER2 COM IS ONLY CALCED WITH GOOD BEACONS
    # some combination of distances and angles
    overallBestFitScore = np.inf
    bestRotation = -1
    # try alignment for all possible 3D roations of scanner2 coords
    for rotation in range(24):
        scanner2 = deepcopy(scanner2Original)

        #rotate scanner 2 coords
        for i, coords in enumerate(scanner2['absBeaconCoords']):
            scanner2['absBeaconCoords'][i] = rotateVec(coords, rotation)

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

            # move all absolute S2 Coords by translation Vec
            newCoords = scanner2['absBeaconCoords'] + translationVec

            # calculate fit score after alignment (mean of minimum distances)
            fitScore = np.mean([num[1]**2 for num in closestS1Beacon])
            
            # if fit score is better: accept newCoords and do another alignment, else break
            if fitScore < prevFitScore: 
                scanner2['absBeaconCoords'] = newCoords
            else: break
        
        if fitScore < overallBestFitScore:
            bestScanner2 = deepcopy(scanner2)
            overallBestFitScore = fitScore
            bestRotation = rotation

    return bestScanner2


def ICPalignLocal(scanner1, scanner2Original):

    overallBestFitScore = np.inf
    bestRotation = -1
    # try alignment for all possible 3D roations of scanner2 coords
    for rotation in range(24):
        scanner2 = deepcopy(scanner2Original)

        #rotate scanner 2 coords
        for i, coords in enumerate(scanner2['absBeaconCoords']):
            scanner2['absBeaconCoords'][i] = rotateVec(coords, rotation)

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

            # move all absolute S2 Coords by translation Vec
            newCoords = scanner2['absBeaconCoords'] + translationVec

            # calculate fit score after alignment (mean of minimum distances)
            fitScore = np.mean([num[1]**2 for num in closestS1Beacon])
            
            # if fit score is better: accept newCoords and do another alignment, else break
            if fitScore < prevFitScore: 
                scanner2['absBeaconCoords'] = newCoords
            else: break
        
        if fitScore < overallBestFitScore:
            bestScanner2 = deepcopy(scanner2)
            overallBestFitScore = fitScore
            bestRotation = rotation

    return bestScanner2

scanner1Aligned = ICPalign(scanners[0], scanners[2])

def plotlists(scanner):
    xl, yl, zl = [], [], []
    for coord in scanner['absBeaconCoords']:
        x,y,z = coord
        xl.append(x)
        yl.append(y)
        zl.append(z)
    
    return [xl, yl, zl]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
print(plotlists(scanners[0]))
ax.scatter(*plotlists(scanners[0]))
ax.scatter(*plotlists(scanners[2]))
ax.scatter(*plotlists(scanner1Aligned))
plt.show()