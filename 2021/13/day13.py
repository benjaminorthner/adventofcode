import numpy as np


with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

# Load in Paper
dots, folds = [], []
inst_reach = False
for line in lines:
    if line == "":
        inst_reach = True
        continue

    if inst_reach:
        dir, loc = line.split("=")
        folds.append((dir[-1], int(loc)))

    if not inst_reach:
        x, y = line.split(",")
        dots.append((int(x),int(y)))

width = max([d[0] for d in dots])
height = max([d[1] for d in dots])

paper = np.zeros((height+1, width+1), dtype=int)
for (x,y) in dots:
    paper[y,x] = 1


def fold(paper, n, dir):
    
    if dir == "x":
        paper = np.transpose(paper)

    for i in range(len(paper[:n])):
        for j in range(len(paper[0])):
            if n < n + (n-i) < len(paper):
                paper[i,j] += paper[n + (n - i),j]

    paper = paper[:n]
    if dir == "x":
        paper = np.transpose(paper)
    
    # convert to 1s
    return np.sign(paper)

# make first fold
for dir, loc in folds[:1]:
    paper = fold(paper, loc, dir)

print(np.count_nonzero(paper))

# PART 2

for dir, loc in folds[1:]:
    paper = fold(paper, loc, dir)
    
for line in paper:
    for c in line:
        if c: print('#', end='')
        else: print(' ', end='')
    print('')
