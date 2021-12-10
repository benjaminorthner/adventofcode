from collections import defaultdict
import re
import math
import numpy as np
from numpy.core.fromnumeric import sort
from collections import deque

with open("input.dat", "r") as file:
    lines = [list(line.strip()) for line in file.readlines()]

illegal_points = 0
illPointDict = {')':3, ']':57, '}':1197, '>':25137}
for line in lines:
    stack = deque()

    for i, bracket in enumerate(line):
        if i == 0:
            stack.append(bracket)
            continue

        if len(stack) > 0 and [stack[-1], bracket] in [['{', '}'], ['[', ']'], ['(', ')'], ['<', '>']]:
            stack.pop()
            continue
        
        stack.append(bracket)

    if len(stack) > 0:
        for b in stack:
            # find illegal char
            if b in illPointDict.keys():
                illegal_points += illPointDict[b]
                break
    
print(illegal_points)


# PART2
def closeme(bracket):
    if bracket == "{": return "}"
    if bracket == "[": return "]"
    if bracket == "<": return ">"
    if bracket == "(": return ")"


pointslist = []
pointsDict = {')':1, ']':2, '}':3, '>':4}
for line in lines:

    stack = deque()

    for i, bracket in enumerate(line):
        if i == 0:
            stack.append(bracket)
            continue

        if len(stack) > 0 and [stack[-1], bracket] in [['{', '}'], ['[', ']'], ['(', ')'], ['<', '>']]:
            stack.pop()
            continue
        
        stack.append(bracket)

    isIllegal = False
    if len(stack) > 0:
        for i, b in enumerate(stack):
            if b in pointsDict.keys():
                isIllegal = True
                break

        # line is illegal
        if isIllegal: continue

        # line is legal
        bstring = [closeme(stack.pop()) for _ in range(len(stack))]
        
        points = 0
        for b in bstring:
            points *= 5
            points += pointsDict[b]
        pointslist.append(points)

print(int(np.median(pointslist)))