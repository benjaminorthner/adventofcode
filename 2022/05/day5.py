from copy import deepcopy

with open("input.dat", "r") as file:
    lines = [line for line in file.readlines()]

initial_config = lines[:lines.index("\n") - 1]
stack_indices = lines[lines.index("\n") - 1]
moves = lines[lines.index("\n") + 1 :]

stack_count = int(stack_indices[-3])
stacks = [[] for _ in range(stack_count)]

# loop over all stacks
for i in reversed(range(len(initial_config))):
    # create list for each row, picking out only letters
    config_list = [initial_config[i][x] for x in [1 + 4*j for j in range(stack_count)]]

    # fill each rows letter into the correct stack
    for istack, letter in enumerate(config_list):
        if letter != ' ':
            stacks[istack].append(letter)

# deepcopy for part2
stacks2 = deepcopy(stacks) 

# Doing the moves
for move in moves:
    # extract numbers from instruction
    # n..number, f... from, t.... to
    _, n, _, f, _, t = move.split(" ")
    n, f, t = int(n), int(f)-1, int(t)-1

    for i in range(n):
        letter = stacks[f].pop()
        stacks[t].append(letter)

# outputting the top crate
part1 = ""
for istack in range(stack_count):
    part1 += stacks[istack][-1]

print(part1)

# Doing the moves for part2
for move in moves:
    _, n, _, f, _, t = move.split(" ")
    n, f, t = int(n), int(f)-1, int(t)-1

    stacks2[t] += stacks2[f][-n:]
    stacks2[f] = stacks2[f][:len(stacks2[f])-n]

# outputting the top crate
part2 = ""
for istack in range(stack_count):
    if len(stacks2[istack]) != 0:
        part2 += stacks2[istack][-1]

print(part2)