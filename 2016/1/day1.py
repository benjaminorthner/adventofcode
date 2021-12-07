import numpy as np

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

positions = lines[0].split(",")

'''
x = 0
y = 0
caxis = "x"
cdir = 1
for p in positions:
    p = p.strip()
    dir = p[0]
    step = int(p[1:])
    
    if caxis == "x" and dir == "R" and cdir == 1:
        caxis = "y"
        cdir = 1
        y += step*cdir
    
    if caxis == "x" and dir == "L" and cdir == 1:
        caxis = "y"
        cdir = -1
        y += step*cdir

    if caxis == "x" and dir == "R" and cdir == -1:
        caxis = "y"
        cdir = -1
        y += step*cdir
    
    if caxis == "x" and dir == "L" and cdir == -1:
        caxis = "y"
        cdir = 1
        y += step*cdir

    if caxis == "y" and dir == "R" and cdir == 1:
        caxis = "x"
        cdir = -1
        x += step*cdir

    if caxis == "y" and dir =="L" and cdir == 1:
        caxis = "x"
        cdir = 1
        x += step*cdir

    if caxis == "y" and dir == "R" and cdir == -1:
        caxis = "x"
        cdir = 1
        x += step*cdir

    if caxis == "y" and dir =="L" and cdir == -1:
        caxis = "x"
        cdir = -1
        x += step*cdir


print(x + y)
'''

x, y = 0, 0
compass = ["N", "W", "S", "E"]
dir = "N"
for p in positions:
    p = p.strip()
    turn = p[0]
    step = int(p[1:])

    # make turn
    if turn == "L":
        dir = compass[(compass.index(dir) + 1) % 4]
    
    if turn == "R":
        dir = compass[(compass.index(dir) - 1) % 4]

    if dir == "N": y += step
    if dir == "S": y -= step
    if dir == "E": x += step
    if dir == "W": x -= step

#print(x + y)


# part 2
# didnt bother
    
    

