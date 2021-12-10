import numpy as np

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]
positions = list(map(int,lines[0].split(",")))

#part1
print(min([sum([np.abs(p - targetP) for p in positions]) for targetP in range(max(positions))]))

#part2
print(min([sum([(lambda x: int((x*(x+1)) / 2))(np.abs(p - targetP)) for p in positions]) for targetP in range(max(positions))]))

