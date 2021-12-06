# super inefficient but it works

with open("input.dat", 'r') as file:
    lines = file.readlines()
    
lines = [int(line) for line in lines]

part1 = 0
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        if lines[i] + lines[j] == 2020:
            part1 = lines[i] * lines[j]

print(f"Part1: {part1}")


part2 = 0
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        for k in range(j + 1 , len(lines)):
            if lines[i] + lines[j] + lines[k] == 2020:
                part2 = lines[i]*lines[j]*lines[k]

print(f"Part2: {part2}")
