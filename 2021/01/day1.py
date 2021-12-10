with open("input.dat", 'r') as file:
    lines = file.readlines()
    
lines = [int(line) for line in lines]



part1 = 0
prev = 0
inc = 0
for i,line in enumerate(lines):
    if i != 0 and line > prev:
        inc += 1
    prev = line
    
print(f"part1: {inc}")

newlines = []
for i in range(len(lines)-2):
    newlines.append(lines[i] + lines[i+1] + lines[i+2])

part1 = 0
prev = 0
inc = 0
for i,line in enumerate(newlines):
    if i != 0 and line > prev:
        inc += 1
    prev = line

print(f"part2: {inc}")


