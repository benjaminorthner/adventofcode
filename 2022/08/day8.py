import numpy as np

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

tMap = np.zeros(shape=(len(lines), len(lines[0])), dtype=int)

for i,line in enumerate(lines):
    for j,c in enumerate(line):
        tMap[i,j] = int(c)

vMap = np.ones(shape=tMap.shape)

for i in range(1, len(tMap)-1):
    for j in range(1, len(tMap[0])-1):

        current  =tMap[i, j]

        left = tMap[i, :j]
        up = tMap[:i, j]
        down = tMap[i+1:, j]
        right = tMap[i, j+1:]

        if current<=max(left) and current<=max(right) and current<=max(up) and current<=max(down):
            vMap[i, j] = 0

part1 = 0
for i in range(len(vMap)):
    for j in range(len(vMap[0])):
        if vMap[i,j] == 1: 
            part1 += 1

print(part1)
# ------
# PART 2
# ------

def sScore(current, treelist):
    score = 0
    for tree in treelist:
        score += 1
        if tree < current:
            continue
        break
    return score

part2 = 0
for i in range(1, len(tMap)-1):
    for j in range(1, len(tMap[0])-1):

        current = tMap[i, j]

        left = tMap[i, :j][::-1]
        up = tMap[:i, j][::-1]
        down = tMap[i+1:, j]
        right = tMap[i, j+1:]

        scenicScore = sScore(current, left) * sScore(current, right)  * sScore(current, up) * sScore(current, down)
        
        if scenicScore > part2:
            part2 = scenicScore

print(part2)