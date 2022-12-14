import numpy as np
from copy import deepcopy

with open("input.dat", 'r') as file:
    lines = [line.strip() for line in file.readlines()]

xcoords = []
ycoords = []

rockLines = []
for line in lines:
    pointGroup = []
    for point in line.split(" -> "):
        x, y = point.split(",")
        x, y = int(x), int(y)

        xcoords.append(x)
        ycoords.append(y)

        pointGroup.append((x, y))
    rockLines.append(pointGroup)
    
xrange = (min(xcoords), max(xcoords))
yrange = (min(ycoords), max(ycoords))

# walls are a set of coords (if it exists there is a rock)
rocks = set()

for rockLine in rockLines:
    for c1, c2 in zip(rockLine, rockLine[1::]):
        dx = c2[0] - c1[0]
        dy = c2[1] - c1[1]

        for i in range(abs(dx) + 1):
            rocks.add(tuple(np.array(c1) + np.array([np.sign(dx) * i,0])))
        for i in range(abs(dy) + 1):
            rocks.add(tuple(np.array(c1) + np.array([0,np.sign(dy) * i])))

        
 
sand = set()

down = np.array([0, 1])
downLeft = np.array([-1, 1])
downRight = np.array([1, 1])


def simulateParticle(particle):
    
    while True:
        if particle[1] > yrange[1]:
            return False

        if tuple(particle + down) not in rocks.union(sand):
            particle += down
            continue
        elif tuple(particle + downLeft) not in rocks.union(sand):
            particle += downLeft
            continue
        elif tuple(particle + downRight) not in rocks.union(sand):
            particle += downRight
            continue
        
        
        return True

def printPicture():
    for y in range(yrange[0] - 10, yrange[1] + 4):
        for x in range(xrange[0] - 5, xrange[1] + 20):
            if (x, y) in rocks:
                print("#", end="")
            elif (x, y) in sand:
                print("o", end="")
            else:
                print(" ", end="")
    
        print("")
    print("")
            


while True:
    newparticle = np.array([500, 0])
     
    simCompleted = simulateParticle(newparticle)

    if simCompleted == True:
        sand.add(tuple(newparticle))
        continue
    else:
        break

printPicture()
part1 = len(sand)
print(part1)

def simulateParticle2(p):

    checkSet = rocks.union(sand)
    while True:
        if p in sand:
            return False, p

        if p[1] > yrange[1]:
            return True, p

        if (p[0], p[1] + 1) not in checkSet:
            p = (p[0], p[1] + 1)
            continue
        elif (p[0]-1, p[1] + 1) not in checkSet:
            p = (p[0]-1, p[1] + 1)
            continue
        elif (p[0]+1, p[1] + 1) not in checkSet:
            p = (p[0]+1, p[1] + 1)
            continue
        
        return True, p

def reduceSand():
    removelist = []
    checkset = sand.union(rocks)
    for s in sand:
        #if (s[0]-1, s[1]) in checkset and (s[0]+1, s[1]) in checkset and (s[0], s[1]-1) in checkset and (s[0], s[1]+1) in checkset:
        if (s[0], s[1]-1) in checkset and (s[0]-1, s[1]-1) in checkset and (s[0]+1, s[1]-1) in checkset:
            removelist.append(s)

    for s in removelist:
        sand.remove(s) 

count = 0
while True:
    newparticle = (500, 0)
     
    simCompleted, newparticle = simulateParticle2(newparticle)

    if simCompleted == True:
        reduceSand() # improves speed but still slow (kinda unnecessary)
        sand.add(newparticle)
        count += 1
        continue
    else:
        break

print(part1 + count)