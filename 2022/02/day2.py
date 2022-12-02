import string

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]


part1 = 0
part2 = 0
for pair in lines:
    # convert letters to position in alphabet (A=0, B=1, ...)
    opp, me = map(string.ascii_uppercase.index, pair.split(" "))

    # map X,Y,Z -> A,B,C
    me -= 23

    if me - opp == 0: part1 += 3 # Draw
    elif me - opp == 1: part1 += 6 # Win
    elif opp - me == 2: part1 += 6 # Win

    # score from choice
    part1 += me + 1

    # here me represents the outcome of the game outcome
    part2 += 3 * me + (opp + (2 + me) % 3) % 3 + 1

print(part1)
print(part2)