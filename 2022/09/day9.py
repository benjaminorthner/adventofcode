import numpy as np

with open("input.dat", "r") as file:
    lines = [line for line in file.readlines()]

# ---- FUNCTIONS ----
def moveHead(H, dir):

    if dir == 'R':
        H[0] += 1
    elif dir == 'L':
        H[0] -= 1
    elif dir == 'U':
        H[1] += 1
    elif dir == 'D':
        H[1] -= 1

def moveKnot(T, H):
    # move tail based on head distance
    dist = np.linalg.norm(H - T)

    # vertical or horizontal moves
    if dist == 2:
        T += (H - T) // 2
    
    # diagonal moves
    elif dist > 2:
        T += np.sign(H - T)



# ---------------------
# PART1: rope_len = 2
# PART2: rope_len = 10
for rope_len in [2, 10]:

    # init rope
    rope = []
    for _ in range(rope_len):
        rope.append(np.array([0,0], dtype=int))

    # initialise path that tail takes
    tail_path = []

    for line in lines:
        dir, steps = line.strip().split(" ")

        for _ in range(int(steps)):

            # move the head
            moveHead(rope[0], dir)

            # move all knots successively
            for knot, prevknot in zip(rope[1:], rope[:-1]):
                moveKnot(knot, prevknot)
            
            # track tail path
            tail_path.append(tuple(rope[-1]))

    print(len(set(tail_path)))