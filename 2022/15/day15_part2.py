# WARNING
# I DON'T KNOW WHY BUT THIS CODE DOES NOT WORK FOR THE SMALL EXAMPLE
# IT WORKS FOR MY INPUT THO
# SUPER WEIRD

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

sensors = []
beacons = []

# parse input
for line in lines:
    words = line.split()
    sensors.append((int(words[2].strip('x=').strip(',')), int(words[3].strip("y=").strip(":"))))
    beacons.append((int(words[8].strip('x=').strip(',')), int(words[9].strip("y=").strip(":"))))

# IMRPOVEMENT
# Technically the missing beacon must appear at a spot right 1 manhatten unit away (in all directions) from an overlao of two signal regions
# so find a list of all points on the boundary of two sensors, then check all points surrounding the boundaries

# every line is defined by two numbers (slop and intercept). Store as tuple (m, c)
def lineFromPoints(x1, y1, x2, y2):
    m = (y1 - y2) // (x1 - x2)
    c = y2 - m*x2
    return (m, c)

searchSpace = (0, 4000000)
lines = set()
for i, (s, b) in enumerate(zip(sensors, beacons)):
    d = manhattan(s, b)

    # find 4 points that we will use to make lines
    x1, y1 = s[0] + d, s[1]
    x2, y2 = s[0], s[1] + d
    x3, y3 = s[0] - d, s[1]
    x4, y4 = s[0], s[1] - d

    # lines between 1->2, 2->3, 3->4, 4->1
    lines.add(lineFromPoints(x1, y1, x2, y2))
    lines.add(lineFromPoints(x2, y2, x3, y3))
    lines.add(lineFromPoints(x3, y3, x4, y4))
    lines.add(lineFromPoints(x4, y4, x1, y1))

# split lines into positive slope and negative slop
posLines = []
negLines = []
                    
for line in lines:
    m, _ = line

    if m > 0:
        posLines.append(line)
    else:
        negLines.append(line)

intersections = []
for pL in posLines:
    for nL in negLines:
        ix = (nL[1] - pL[1]) // 2
        iy = (nL[1] + pL[1]) // 2 

        if searchSpace[0] <= ix <= searchSpace[1] and searchSpace[0] <= iy <= searchSpace[1]:
            intersections.append((ix, iy))


solutions = []
for inter in intersections:

    for x, y in [(inter[0]-1, inter[1]), (inter[0] + 1, inter[1]), (inter[0], inter[1] - 1), (inter[0], inter[1] + 1)]:

        # again check if in search space
        if not(searchSpace[0] <= x <= searchSpace[1] and searchSpace[0] <= y <= searchSpace[1]):
            continue

        outsideAllRanges = True
        for s, b in zip(sensors, beacons):

            dToSensor = manhattan((x, y), s)
            dSensorToBeacon = manhattan(s, b)

            # if distance to sensor is within or equal to sensor range, and the current spot is not already a beacon,
            # then new definitely unoccupied spot is found, break after finding to not overcount
            if dToSensor <= dSensorToBeacon:
                outsideAllRanges = False
                break
            
        if outsideAllRanges:
            solutions.append((x,y))
            break
    
    if len(solutions) == 1:
        break

print(solutions[0][0] * 4000000 + solutions[0][1])