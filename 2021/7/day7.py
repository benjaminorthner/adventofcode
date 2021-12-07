import numpy as np

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]
positions = list(map(int,lines[0].split(",")))

# part 1
spendlist = [sum([np.abs(p - targetP) for p in positions]) for targetP in range(max(positions))]
print(min(spendlist))

# part 2
sumallbelow = lambda x: int((x*(x+1)) / 2)
spendlist = [sum([sumallbelow(np.abs(p - targetP)) for p in positions]) for targetP in range(max(positions))]
print(min(spendlist))
