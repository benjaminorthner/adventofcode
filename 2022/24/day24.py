from collections import deque

with open('input.dat', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

# get map dimensions
mapWidth = len(lines[0]) - 2
mapHeight = len(lines) - 2 

# blizzards repeat every blizzardPeriod
blizzardPeriod = mapHeight * mapWidth

# define arrows and corresponding directions
arrows = ['>', 'v', '<', '^']
D = ((0, 1), (1, 0), (0, -1), (-1, 0))

# parse lines and add blizzards to set
# Note coordinate (0,0) is the top left '.' contained within the valley
blizzards = set()
for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] in arrows:
            blizzards.add((y-1,x-1,arrows.index(lines[y][x])))

def moveBlizzards(blizzards):
    newBlizzards = set()
    for blizzard in blizzards:
        newY = (blizzard[0] + D[blizzard[2]][0]) % mapHeight
        newX = (blizzard[1] + D[blizzard[2]][1]) % mapWidth
        newBlizzards.add((newY, newX, blizzard[2]))
    
    return newBlizzards

def getBlizzardCoordinates(blizzards):
    return  [(y, x) for y, x, _ in blizzards]

# only needed for printing map
def countOverlaps(y, x, blizzards):
    blizzardCoordList = getBlizzardCoordinates(blizzards) 
    return blizzardCoordList.count((y, x))

def getBlizzardSign(yy, xx, blizzards):
    try:
        return arrows[[d for y, x, d in blizzards if y == yy and x == xx][0]]
    except:
        return None

def printMap(blizzards):
    blizzardCoordinates = set([(y, x) for y, x, _ in blizzards])

    print("#.", end="")
    print("#"*mapWidth)
    for y in range(mapHeight):
        print("#", end="")
        for x in range(mapWidth):
            overlapCount = countOverlaps(y, x, blizzards)
            
            if overlapCount > 1:
                print(overlapCount, end="")
            elif overlapCount == 1:
                print(getBlizzardSign(y, x, blizzards), end="")
            else:
                print('.', end="")
        print("#")
    print("#"*mapWidth, end="")
    print(".#\n")

def manDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# keeps only the n best performing states in the queue (to reduce the state space)
# heuristic is manhattan distance to the end
def pruneQueue(Q, n, end):
    if len(Q) < n:
        return Q

    newQ = deque()
    # find distance to end of every Queue item
    dList = [manDistance(coord, end) for coord, _ in Q]
    cutoff = sorted(dList)[n - 1]
    for item in Q:
        if manDistance(item[0], end) <= cutoff:
            newQ.append(item)
    return newQ
        
        

# for my input beamWidth 80 is needed for the correct result.
def bfs(blizzards, beamWidth=100, reverse=False):

    # append start + time elapsed since start (=0)
    Q = deque()
    start = (-1,0)
    end = (mapHeight, mapWidth-1)
    if reverse:
        start, end = end, start
    Q.append((start, 0))
    blizzardCoordinates = getBlizzardCoordinates(blizzards)

    prevT = 0
    S = set()
    while Q:
        (y, x), t = Q.popleft()
        currentT = t

        #  evolve blizzard and check if neighbouring positions 
        # (and current position) are non-blizzard-occupied
        if currentT > prevT:
            blizzards = moveBlizzards(blizzards)
            blizzardCoordinates = getBlizzardCoordinates(blizzards) 

            # prune the queue by keeping only the n spots closest to the end
            # This is also called a BeamSearch
            Q = pruneQueue(Q, n= beamWidth, end=end)


        # if end is reached return time taken
        if (y, x) == end:
            return t - 1, blizzards

        # makes sure if the same position is reached after a bilzzardPeriod has passed then it shall not be checked further 
        # since the result can not be better than reaching it in a previous period
        # period thing has no real improvement tho because t never goes that far. So improvement for different paths coming into same spot at same t
        if (((y, x), t % blizzardPeriod)) in S:
            continue
        S.add(((y, x), t))

        for dy, dx in [(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1)]:
            newY = y + dy
            newX = x + dx

            # check that newPosition lies within the map
            if (newY < 0 or newY >= mapHeight or newX < 0 or newX >= mapWidth) and (newY, newX) not in [start, end]:
                continue

            # check if newPosition is available
            if (newY, newX) not in blizzardCoordinates:
                Q.append(((newY, newX), t + 1))
        
        prevT = currentT

    # if the end is never reached and the Queue is emptied
    return None, blizzards

part1, blizzards1 = bfs(blizzards)
print(part1)

# NOTE once we hit a checkpoint (start or end) it is enough to take the fastest path there as a starting point
# there is no way a slower initial path can lead to a faster later path because this later path could also be reached
# by simply waiting at the checkpoint until the time comes 

# go back to beginning starting with end blizzard state
part2 = part1
tBackToStart, blizzards2 = bfs(blizzards1, reverse=True)

# go back to end starting with previous ending blizzard state
part2+= tBackToStart + 1
tBacktoFinish, _ = bfs(blizzards2)

part2 += tBacktoFinish + 1
print(part2)