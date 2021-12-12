from collections import defaultdict, deque
from copy import deepcopy

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

# create adjacency list of neighbours
neighbours = defaultdict(set)
for line in lines:
    dep, arr = line.split("-")
    neighbours[dep].add(arr)
    neighbours[arr].add(dep)

def BFS(start, end, part2=False):
    pathcount = 0
    queue = deque()
    queue.append((start, set([start]), None))
    # while queue not empty keep going
    while queue:
        # unpack elements next in line of the queue
        currentNode, smallVisited, visitedTwice = queue.popleft()

        # if the end is found, move to next in queue to find another path
        if currentNode == end:
            pathcount += 1
            continue

        # loop through neighbours of current cave
        # requires deepcopy of visited dict so that, other smallVisited dicts in queue arent affected
        for n in neighbours[currentNode]:
            # don't loop over already visited caves
            if n not in smallVisited:
                smallVisitedCopy = deepcopy(smallVisited)
                # if new node is a small cave, add it to the visited small cave set
                if n.islower():
                    smallVisitedCopy.add(n)
                queue.append((n, smallVisitedCopy, visitedTwice))

            # for part2 when nothing has been visited twice yet and currentCave n is small and has been visted before
            elif (n in smallVisited) and (n not in ["start", "end"]) and (visitedTwice is None) and part2:
                queue.append((n, smallVisited, n))
    
    return pathcount

print(BFS("start", "end"))
print(BFS("start", "end", part2=True))
