from collections import defaultdict
import numpy as np
from copy import deepcopy


with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

_, data = lines[0].split(": ")
xdata, ydata = data.split(", ")
_, xrangedata  = xdata.split("=")
_, yrangedata = ydata.split("=")

xmin, xmax = xrangedata.split("..")
xmin = int(xmin)
xmax = int(xmax)

ymin, ymax = yrangedata.split("..")
ymin = int(ymin)
ymax = int(ymax)


def simulateFlight(vx, vy, xmin, xmax, ymin, ymax, returnTraj = False):

    xpos = 0
    ypos = 0
    maxheight = ypos
    traj = [(xpos, ypos)]

    while True:
        # update max y
        if ypos > maxheight : maxheight = ypos

        # check if in the target
        if ypos in range(ymin, ymax + 1) and xpos in range(xmin, xmax + 1):
            if not returnTraj:
                return maxheight, "onTarget", True
            else:
                return maxheight, "onTarget", True, traj
        
        if np.sign(vx) == 1:
            if np.sign(vx) != np.sign(xmax - xpos):
                if not returnTraj:
                    return None, "missedRight", False
                else:
                    return None, "onTarget", False, traj
        
        elif np.sign(vx) == -1:
            if np.sign(vx) != np.sign(xmin - xpos):
                if not returnTraj:
                    return None, "missedLeft", False
                else:
                    return None, "missedLeft", False, traj

        elif ypos < ymin and np.sign(vy) == -1:
            if not returnTraj:
                return None, "droppedBelow", False
            else:
                return None, "droppedBelow", False, traj

        ypos += vy
        xpos += vx
        traj.append((vx, vy))

        # drag in x direction only
        vx += -1 * np.sign(vx)

        # gravity
        vy -= 1

###################################### PART 1 (efficient search) ###################################### 

vy = 0
vx = 0
vxOnTarget = defaultdict(lambda: [])
prevMaxHeight = 0
failcount = 0
while True:
    while True:
        maxheight, message, targetHit = simulateFlight(vx, vy, xmin, xmax, ymin, ymax)

        if maxheight is not None:
            if maxheight > prevMaxHeight:
                prevMaxHeight = maxheight

        if targetHit:
            vxOnTarget[vy].append(vx)

        # keep increasing vx until we overshoot to the right
        if message != "missedRight":
            vx += 1
            continue

        break
    
    # break if no more on target hits are found failcount amount of times
    if len(vxOnTarget[vy]) == 0:
        if failcount <= 100:
            failcount += 1
            vx = min(vxOnTarget[0])
            vy += 1
            continue
        break

    # set initial vx to minimum that managed to hit with previous vy
    vx = min(vxOnTarget[vy])

    # increase vy
    vy += 1

#print(prevMaxHeight)


###################################### PART 1 & 2 (NASTY BRUTE FORCE) ###################################### 

VX = range(0, 200)
VY = range(-140, 200)
maxheight = 0
count = 0
for vx in VX:
    for vy in VY:

        height, _, hit = simulateFlight(vx, vy, xmin, xmax, ymin, ymax)
        
        if height is not None:
            if height > maxheight:
                maxheight = height

        if hit:
            count += 1

print(maxheight)
print(count)