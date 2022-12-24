with open('input.dat', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

# add every elves coord into a set
def parseInput():
    elves = set()
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == "#":
                d = 0 # direction the elf will consider first
                # object is y & x coords of elf, d is direction he will consider first and None 
                # is a placeholder for (x,y,d) y&x&d of where elf wants to move
                elves.add((y, x, d, None))
    return elves

# directions elves consider moving in
D = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def hasNeighbour(y, x, elfCoordinates):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (y + dy, x + dx) in elfCoordinates and (dy, dx) != (0, 0):
                return True
    return False

def findNextPosition(x, y, d, elfCoordinates):
    for dd in range(4):
        tryD = (d+dd)%4
        tryY = y + D[tryD][0]
        tryX = x + D[tryD][1]
        if (tryY, tryX) in elfCoordinates or (tryY + D[tryD][1], tryX + D[tryD][0]) in elfCoordinates or (tryY - D[tryD][1], tryX - D[tryD][0]) in elfCoordinates:
            continue
        return (tryY, tryX)
    
    # if no possible move return None
    return None

def getElfCoordinates(elves):
    return set([(y, x) for y, x, _, _ in elves])

def findRectangle(elves):
    yrange = (min([y for y, *_ in elves]), max([y for y, *_ in elves]) + 1)
    xrange = (min([x for _, x, *_ in elves]), max([x for _, x, *_ in elves]) + 1)
    return yrange, xrange

def printMap(elves):
    elfCoordinates = getElfCoordinates(elves)
    # find map ranges
    yrange, xrange = findRectangle(elves)

    for y in range(yrange[0]-1, yrange[1]+1):
        for x in range(xrange[0]-1, xrange[1]+1):
            if (y, x) in elfCoordinates:
                print("#", end="")
            elif (y, x) == (0 , 0):
                print("X", end="")
            else:
                print(" ", end="")
        print("")
    print("")

def diffuse(elves):
    someElvesMoved = False
    # STEP 1 
    # (Prime elves with new positions they want to go to)
    elvesAfterStep1 = set()
    elfCoordinates = getElfCoordinates(elves) 
    for y, x, d, _ in elves:
        # if elf does not have neighbour, then move on to next elf
        if not hasNeighbour(y, x, elfCoordinates):
            elvesAfterStep1.add((y, x, d, (y, x)))
            continue

        # if this point is reached some elves will move / try to move
        someElvesMoved = True
        # elf chooses a move in a direction with no other elf
        newElfPosition = findNextPosition(x, y, d, elfCoordinates)
        if newElfPosition == None:
            elvesAfterStep1.add((y, x, d, (y, x)))
            continue
        elvesAfterStep1.add((y, x, d, newElfPosition))

    # STEP 2 
    # (Try moving each elf, if there is a clash elves stay put)
    elvesAfterStep2 = set()
    newElfPositions = [newPos for _, _, _, newPos in elvesAfterStep1]
    for y, x, d, newPosition in elvesAfterStep1:
        
        # if clash then put old position into set
        if newElfPositions.count(newPosition) > 1:
            elvesAfterStep2.add((y, x, d + 1, None))
        
        # otherwise put in newposition
        else:
            elvesAfterStep2.add((*newPosition, d + 1, None))
    
    return elvesAfterStep2, someElvesMoved

def calcEmptyGround(elves):
    yrange, xrange = findRectangle(elves)
    elfCoordinates = getElfCoordinates(elves)

    count = 0
    for y in range(*yrange):
        for x in range(*xrange):
            if (y, x) not in elfCoordinates:
                count += 1
    return count

# ------
# PART 1
# ------
elves = parseInput()

# diffuse 10x
for _ in range(10):
    elves, _ = diffuse(elves)

printMap(elves)
print(calcEmptyGround(elves))

# ------
# PART 2
# ------
# SLOW BUT WORKS (takes about a min)

elves = parseInput()
someElvesMoved = True
roundNumber = 0
while someElvesMoved:
    elves, someElvesMoved = diffuse(elves)
    roundNumber += 1

printMap(elves)
print(roundNumber)



        




            



