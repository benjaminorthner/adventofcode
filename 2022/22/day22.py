from copy import deepcopy
from time import sleep

with open('input.dat', 'r') as file:
    gMap, movementString = file.read().split("\n\n")
    gMap = gMap.split("\n")
    mapWidth = len(gMap[0])

# make all lines in map equal length by padding the ends with spaces
def initMap():
    maxWidth = max([len(row) for row in gMap])
    for i in range(len(gMap)):
        if len(gMap[i]) < maxWidth:
            gMap[i] = gMap[i] + " " * (maxWidth - len(gMap[i]))

        # turn string into list
        gMap[i] = list(gMap[i])


# split movementString into letters and numbers
def parseMovements():
    movements = []
    currentNumberString = ''
    for i in range(len(movementString)):
        if movementString[i].isdigit():
            currentNumberString += movementString[i]
            # if end of string then append number as is
            if i == len(movementString) - 1:
                movements.append(int(currentNumberString))
        else:
            if currentNumberString != '':
                movements.append(int(currentNumberString))
                currentNumberString = ''

            movements.append(movementString[i])
    
    return movements

def column(matrix, c):
    return [row[c] for row in matrix]

# find col in which the map starts
def findStart():
    c = 0
    for i in range(len(gMap[r])):
        if gMap[r][i] != '.':
            c += 1
        else:
            break
    return c

def getIndex(gMap, x):
    try:
        return gMap.index(x)
    except:
        return 10000000

def printToVis(r, c, d):
    visMap[r][c] = '>' if d == 0 else 'v' if d == 1 else '<' if d == 2 else '^'

def printMap():
    with open('outMap.txt', 'w+') as f:
        for line in visMap:
            print("".join(line), file=f)

def getStartAndWidth(row, col):
    rStart = min([column(gMap, col).index('.'), column(gMap, col).index('#')])
    rWidth = sum([column(gMap, col).count('.'), column(gMap, col).count('#')])
    
    cStart = min([getIndex(gMap[row], '.'), getIndex(gMap[row], '#')])
    cWidth = sum([gMap[row].count('.'), gMap[row].count('#')])

    return (rStart, rWidth, cStart, cWidth)

def rotate(move, d):
    if move == 'R':
        newD = (d + 1) % 4
        printToVis(r, c, d)
    elif move == 'L':
        newD = (d - 1) % 4
        printToVis(r, c, d)

    return newD

def getFaceId(r, c):
    tileWidth = mapWidth // 3

    rIndex = r // tileWidth
    cIndex = c // tileWidth

    idList = [[None, 1, 2], [None, 3, None], [4, 5, None], [6, None, None]]
    return idList[rIndex][cIndex]


# find starting position on map & define directions
D = [(0, 1), (1, 0), (0, -1), (-1, 0)] # possible directions
r = 0
c = findStart()
d = 0 # index of current direction in D

# initialise maps and parse movements
initMap()
movements = parseMovements()
visMap = deepcopy(gMap)

#print initial position to visMap
printToVis(r, c, d)
for i, move in enumerate(movements):
    if move in ['L', 'R']:
        d = rotate(move, d)

    else:
        rStart, rWidth, cStart, cWidth = getStartAndWidth(r, c)

        for _ in range(move):
            # new r and c after move
            rr = ((r - rStart) + D[d][0]) % rWidth + rStart
            cc = ((c - cStart) + D[d][1]) % cWidth + cStart
            # if new position is a wall then do nothing
            if gMap[rr][cc] == '#':
                continue

            # else set r and c and continue
            r = rr
            c = cc

            printToVis(r, c, d)
            
print(1000*(r+1) + 4*(c+1) + d)
printMap()


#------
# PART2
#------

# I will index the faces of the cube as follows
# - 1 2
# - 3 -
# 4 5 -
# 6

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
r = 0
c = findStart()
d = 0


# initialise maps and parse movements
initMap()
movements = parseMovements()
visMap = deepcopy(gMap)

#print initial position to visMap
printToVis(r, c, d)
for i, move in enumerate(movements):
    if move in ['L', 'R']:
        d = rotate(move, d)

    else:
        rStart, rWidth, cStart, cWidth = getStartAndWidth(r, c)
        faceId = getFaceId(r, c)
        # TODO keep working on code here
        for _ in range(move):
            # new r and c after move
            rr = ((r - rStart) + D[d][0]) % rWidth + rStart
            cc = ((c - cStart) + D[d][1]) % cWidth + cStart
            # if new position is a wall then do nothing
            if gMap[rr][cc] == '#':
                continue

            # else set r and c and continue
            r = rr
            c = cc

            printToVis(r, c, d)
            
print(1000*(r+1) + 4*(c+1) + d)