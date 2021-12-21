from collections import defaultdict, deque
import re
from copy import deepcopy
import math
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt
from matplotlib import colors

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

####################### PART 1 ##########################
p1_pos = 10
p2_pos = 4
p1_score=0
p2_score=0
die = 1
rollcount = 0

while True:
    for _ in range(3):
        p1_pos = (p1_pos + die - 1)%10 + 1
        die += 1
        rollcount+=1
    p1_score += p1_pos

    if p1_score >=1000:
        break

    
    for _ in range(3):
        p2_pos = (p2_pos + die - 1)%10 + 1
        die += 1
        rollcount+=1
    p2_score += p2_pos

    if p2_score >=1000:
        break

if p1_score > p2_score:
    print(p2_score * rollcount)
else:
    print(p1_score*rollcount)



####################### PART 2 Recursive + Memory ##########################

possible_die_sums = [i+j+k for i in [1,2,3] for j in [1,2,3] for k in [1,2,3]]

# keep track of the wins that followed from a set of positions and scores
memory = {}
def count_wins(p1_pos, p2_pos, p1_score, p2_score):

    # stop condition for recursion
    if p1_score >= 21:
        return [1, 0]
    elif p2_score >= 21:
        return [0, 1]

    # if we already know who will win from this state then just return those wins
    if (p1_pos, p2_pos, p1_score, p2_score) in memory:
        return memory[(p1_pos, p2_pos, p1_score, p2_score)]

    # if not set the win counts to 0 and simulate one round of the game
    win_counter = [0, 0]

    for die in possible_die_sums:
        pp1_pos = (p1_pos + die - 1) % 10 + 1
        pp1_score = p1_score + pp1_pos

        # now its p2s turn to play. Since first player in function plays we swap positions
        [w2, w1] = count_wins(p2_pos, pp1_pos, p2_score, pp1_score)
        # add the wins from this position onwards to the counter (swap back players)
        win_counter[0] += w1
        win_counter[1] += w2
    
    # put the win count from the start state into memory
    memory[(p1_pos, p2_pos, p1_score, p2_score)] = win_counter
    return win_counter
    
print(max(count_wins(10, 4, 0, 0)))



####################### PART 2 BRUTE FORCE DFS (way too slow) ##########################
'''
possible_die_sums = [i+j+k for i in [1,2,3] for j in [1,2,3] for k in [1,2,3]]

wins = [0,0]
cnt = 0
positions = [10,4]
scores = [0,0]
# run through all possible games in DFS manner
stack = deque()
stack.append((*positions, *scores))

while stack:
    if cnt%100000 == 0:
        print(wins)
    cnt+=1
    # remove last set of positions from stack
    p1_pos_prev, p2_pos_prev, p1_score_prev, p2_score_prev = stack.pop()
    
    # go through all possible next moves for p1 and p2
    for dieP1 in possible_die_sums:
        p1_pos, p1_score = p1_pos_prev, p1_score_prev

        p1_pos = (p1_pos + dieP1 - 1) % 10 +1
        p1_score += p1_pos
        
        if p1_score >=21:
            wins[0] += 1
            continue

        for dieP2 in possible_die_sums:
            p2_pos, p2_score = p2_pos_prev, p2_score_prev

            p2_pos = (p2_pos + dieP2 - 1) % 10 + 1
            p2_score += p2_pos

            if p2_score >= 21:
                wins[1] += 1
                continue
            else:
                stack.append((p1_pos, p2_pos, p1_score, p2_score))

print(scores)
print(wins)
'''