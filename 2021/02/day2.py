with open("input.dat", 'r') as file:
    lines = file.readlines()
    
    x = 0
    z = 0
for line in lines:
    direction = (line[:line.index(" ")])
    steps = int(line[line.index(" ") + 1:])

    
    if direction == "forward":
        x += steps
    elif direction == "down":
        z += steps
    elif direction == "up":
        z -= steps


print("part1: ", x*z)


x= 0
z= 0
aim=0
for line in lines:
    direction = (line[:line.index(" ")])
    steps = int(line[line.index(" ") + 1:])
    
    if direction == "forward":
        x += steps
        z += aim*steps
        
    elif direction == "down":
        aim += steps
    elif direction == "up":
        aim -=steps
        
print("part2: ", x*z)