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

# to figure out for which x range we should check the given row
# we first find the min and max x at which a beacon could not be
xrange = [1e20, -1e20]
for s, b in zip(sensors, beacons):
    d = manhattan(s, b)

    if s[0] - d < xrange[0]:
        xrange[0] = s[0] - d

    if s[0] + d > xrange[1]:
        xrange[1] = s[0] + d


# traverse the specified row
print("IT WORKS BUT ITS SUUPER SLOW... sorry\n")
part1 = 0
y = 10
for i, x in enumerate(range(*xrange)):
    # display percentage of calc completed (cause it takes a few min)
    print(f"\r{100*i / (xrange[1] - xrange[0]):.3f} %", end="")
    for s, b in zip(sensors, beacons):
        # check if (x, y) is within any sensors range

        dToSensor = manhattan((x,y), s)
        dSensorToBeacon = manhattan(s, b)

        # if distance to sensor is within or equal to sensor range, and the current spot is not already a beacon,
        # then new definitely unoccupied spot is found, break after finding to not overcount
        if dToSensor <= dSensorToBeacon and (x,y) not in beacons:
            part1 += 1
            break

# clear percentage counter
print("\r        ", end="\r")

print(f"part1: {part1}")