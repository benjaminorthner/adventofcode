import string

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

part1 = 0
for line in lines:
    (c1, c2) = (line[:len(line) // 2], line[len(line) // 2:])
    item = set(c1).intersection(set(c2)).pop()
    part1 += string.ascii_letters.index(item) + 1
print(part1)


part2 = 0
for group in range(len(lines) // 3):
    a, b, c = lines[group*3], lines[1+group*3], lines[2+group*3]
    badge = set(a).intersection(set(b), set(c)).pop()
    part2 += string.ascii_letters.index(badge) + 1
print(part2)