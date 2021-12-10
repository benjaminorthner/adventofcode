with open("input.dat", 'r') as file:
    lines = [int(line) for line in file.readlines()]

# part1
print(sum([ 1 if b>a else 0 for a,b in zip(lines, lines[1::])]))

# part2
lines2 = [a+b+c for a,b,c in zip(lines, lines[1::], lines[2::])]
print(sum([ 1 if b>a else 0 for a,b in zip(lines2, lines2[1::])]))


