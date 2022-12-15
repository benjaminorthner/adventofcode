with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

sensors = []
beacons = []

# parse input
for line in lines:
    words = line.split()
    sensors.append((int(words[2].strip('x=').strip(',')), int(words[3].strip("y=").strip(":"))))
    beacons.append((int(words[8].strip('x=').strip(',')), int(words[9].strip("y=").strip(":"))))

# create list of positions where a beacon cannot be
unoccupied = set()
for i, (s, b) in enumerate(zip(sensors, beacons)):
    print(i)
    # manhattan distance between  & closest beacon pair
    d = abs(s[0] - b[0]) + abs(s[1] - b[1])

    # traverse all coordinates within manhattan distance d of beacon
    # traverse a triangle around d and then use symmetry to obtain other quadrants
    for dy in reversed(range(0, d+1)):
        for dx in range(0, d + 1 - dy):

           # symmetry transformations 
            for dx in [dx, -dx]:
                for dy in [dy, -dy]:
                    # create new unoccupied spot, except if beacon already there
                    new = (s[0] + dx, s[1] - dy)
                    if new not in unoccupied.union(set(beacons)):
                        unoccupied.add(new)
                        print(len(unoccupied))


# count how many spots in row 'checkrow' are unoccupied by beacons
# THIS WORKS FOR THE SMALL EXAMPLE, BUT WAYYY TOO SLOW FOR PROPER EXAMPLE
checkrow = 2000000
print(sum([1 if x[1] == checkrow else 0 for x in unoccupied]))

# print out the map
'''
for j in range(-10, 33):
    for i in range(-10, 33):

        if (i, j) in sensors:
            print("S", end="")
        elif (i, j) in unoccupied:
            print("#", end="")
        elif (i, j) in beacons:
            print("B", end="")
        else:
            print(" ", end="")
    print("")
'''