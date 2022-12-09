import numpy as np

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

def calcSignalStrength(cycle, x):
    if cycle in [20, 60, 100, 140, 180, 220]:
        return x * cycle
    return 0

def blitSprite(image, x):
    spritePos = x
    crtPos = len(image) % 40
    # if sprite is in current pixel
    if abs(crtPos - spritePos) <= 1:
        image += '#'
    else:
        image += '.'
    return image
    


# initialise image for part2
image = ""

cycle = 1
x = 1
part1 = 0
for line in lines:
    
    # split line into instruction and value
    instruction, *val = line.split(" ")
    
    # noop
    if instruction == "noop":
        image = blitSprite(image, x)
        cycle += 1
        part1 += calcSignalStrength(cycle, x)
        continue

    # addx
    val = int(val[0])
    
    image = blitSprite(image, x)
    cycle += 1
    part1 += calcSignalStrength(cycle, x)

    image = blitSprite(image, x)
    x += val
    cycle += 1
    part1 += calcSignalStrength(cycle, x)

print(part1)

for i in range(9):
    print(image[40*i:40*(i+1)])