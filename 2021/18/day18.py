import regex
from copy import deepcopy
from ast import literal_eval

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

def processExplosion(number, left, right):

    # finds the right neighbour of explosion site
    rneighbours = regex.findall("(?<=x[\[,\],\,]+)\d+", number)
    if rneighbours:
        # replace next number on the right with the sum
        number = regex.sub("(?<=x[\[,\],\,]+)\d+", str(int(right) + int(rneighbours[0])), number)

    lneighbours = regex.findall("\d+(?=[\[,\],\,]+x)", number)
    if lneighbours:
        # replace next number on the right with the sum
        number = regex.sub("\d+(?=[\[,\],\,]+x)", str(int(left) + int(lneighbours[0])), number)

    # replace 'x' with 0
    number = regex.sub("x", "0", number)

    return number 

def reduce(number):
    # keep reducing until no more reductions possible
    while True:
        allExploded = True
        allSplit = True
        depth = 0
        # use regex so that real numbers get caught entirely (not just digit wise)
        for pos, char in enumerate(regex.findall(r"([\[,\,\]]|\d+)", number)):
            # loop through string and keep track of depth by counting brackets
            charList = regex.findall(r"([\[,\,\]]|\d+)", number)
            if char == '[': depth += 1
            if char == ']': depth -= 1
            
            # explode
            if depth == 5:
                # extract pair that is to be exploded
                left = charList[pos + 1]
                right = charList[pos + 3]
                # change it out for 'x' so processExplosion function knows where to look
                # very shitty fix where I roughly cut out part I need and perform regex on that
                # (prevents accidentally targeting wrong pair that contains same left and right)
                number =number[:pos] + regex.sub(f"(?<!\[{left}\,{right}\].+)\[{left}\,{right}\]", "x", number[pos:])
                number = processExplosion(number, left, right)
                allExploded = False
                break

        # only start splitting after all explosions done 
        if allExploded:
            # split
            for char in regex.findall(r"([\[,\,\]]|\d+)", number):
                if char not in [',', '[', ']']:
                    if int(char) >= 10:
                        splitPair = f"[{int(char)//2},{int(char) - int(char)//2}]"
                
                        # matches and replaces 2 digit numbers with no other two digit numbers to their left (i.e. leftmost int>=10)
                        number = regex.sub(r"(?<!\d{2,}.+)\d{2,}", splitPair, number)

                        allSplit = False
                        break
            
        if allExploded and allSplit:
            return number

def magnitude(number, str=True):
    if str:
        number = literal_eval(number)

    if isinstance(number, int):
        return number

    left, right = number
    return 3*magnitude(left, False) + 2*magnitude(right, False)

############### PART 1 ##############   
sum = []
for i, line in enumerate(lines):

    # skip first iteration
    if i == 0:
        sum = deepcopy(line)
        continue

    # add two lines
    sum = f"[{sum},{line}]"
    sum = deepcopy(reduce(sum))

print(magnitude(sum))

############### PART 2 (super inefficient and slow) ##############  

maxMag = 0
for i, L1 in enumerate(lines):
    for L2 in lines[i+1:]:
        sum = magnitude(reduce(f"[{L1},{L2}]"))
        if sum > maxMag: maxMag = sum

        sum = magnitude(reduce(f"[{L2},{L1}]"))
        if sum > maxMag: maxMag = sum

print(maxMag)