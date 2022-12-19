from collections import deque

with open('input.dat', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

# extract Blueprints
blueprints = []
for line in lines:
    w = line.split()
    blueprints.append((int(w[6]), int(w[12]), int(w[18]), int(w[21]), int(w[27]), int(w[30])))

def bfs(costlist, time):
    	
    # init queue and append first list of items ((ore, clay, obsidian, geode), (orerobot, clayrobot, obisdianrobot, geoderobot), minutes)
    Q = deque()
    Q.append(((0, 0, 0, 0), (1, 0, 0, 0), 0))
    seenStates = set()
    maxGeodesMined = 0

    maxOreCost = max([costlist[0], costlist[1], costlist[2], costlist[4]])
    maxClayCost = costlist[3]
    maxObsidianCost = costlist[5]

    while Q:
        ores, robots, minutes = Q.popleft()
        
        # after time min check if new maxGeodes mined is found and move onto next in queue (continue)
        if minutes == time:
            if ores[3] > maxGeodesMined:
                maxGeodesMined = ores[3]
            continue
            
        # OPTIMIZATIONS

        # Since every cycle we can only build 1 robot, we do not need more robots than the highest cost of the resource that robots produce
        # example. If the max ore cost for something is 4, then we don't need more than 4 ore robots, cause we could never spend all the ore otherwise
        # we don't restrict geode robots cause we want as many of those as possible
        if robots[0] > maxOreCost: robots = (maxOreCost, robots[1], robots[2], robots[3])
        if robots[1] > maxClayCost: robots = (robots[0], maxClayCost, robots[2], robots[3]) 
        if robots[2] > maxObsidianCost: robots = (robots[0], robots[1], maxObsidianCost, robots[3])

        # similarly as above we don't need to stockpile materials either. If we have enough materials at the current time to buy any robot every cycle
        # until the end, then we don't need any more and can cut off the ore value there, reducing the state space
        # Formula: (most material we would possibly need till the end) - (total material that current robots will have produced by the end)
        maxOreNeeded = maxOreCost * (time - minutes) - robots[0] * (time - minutes - 1)
        maxClayNeeded = maxClayCost * (time - minutes) - robots[1] * (time - minutes - 1)
        maxObisdianNeeded = maxObsidianCost * (time - minutes) - robots[2] * (time - minutes - 1)
        if ores[0] > maxOreNeeded: ores = (maxOreNeeded, ores[1], ores[2], ores[3])
        if ores[1] > maxClayNeeded: ores = (ores[0], maxClayNeeded, ores[2], ores[3])
        if ores[2] > maxObisdianNeeded: ores = (ores[0], ores[1], maxObisdianNeeded, ores[3])

        # check if this state has been reached before and if so skip computation
        # its okay to not check minutes because if the same state is reached at a later time
        # it will definitely not perform better 
        # because BFS later times always come after earlier times
        if (ores, robots) in seenStates:
            continue
        seenStates.add((ores, robots))

        # Generate neighbouring nodes, i.e. gen ore and robot list for what would happen
        # first need to find what we can afford. How many of each robot can we afford.
        # then loop over every possible combination of purchases we could make. Each will be a new node

        # ASSUME THAT EVERY MINUTE WE PURCHASE AT MOST 1 ROBOT
        canAffordOreRobot = ores[0] >= costlist[0]
        canAffordClayRobot = ores[0] >= costlist[1]
        canAffordObsidianRobot = ores[0] >= costlist[2] and ores[1] >= costlist[3]
        canAffordGeodeRobot = ores[0] >= costlist[4] and ores[2] >= costlist[5]

        robotOptions = set()
        if canAffordGeodeRobot:
            r = (robots[0], robots[1], robots[2], robots[3] + 1)
            o = (ores[0] - costlist[4], ores[1], ores[2] - costlist[5], ores[3])
            robotOptions.add((o, r))

        if canAffordObsidianRobot:
            r = (robots[0], robots[1], robots[2] + 1, robots[3])
            o = (ores[0]- costlist[2], ores[1] - costlist[3], ores[2], ores[3])
            robotOptions.add((o, r))

        if canAffordClayRobot:
            r = (robots[0], robots[1] + 1, robots[2], robots[3])
            o = (ores[0] - costlist[1], ores[1], ores[2], ores[3])
            robotOptions.add((o, r))

        if canAffordOreRobot:
            r = (robots[0] + 1, robots[1], robots[2], robots[3])
            o = (ores[0] - costlist[0], ores[1], ores[2], ores[3])
            robotOptions.add((o, r))


        # always add the option to do nothing
        robotOptions.add((ores, robots))

        # for each option update the ore numbers to include the newly mined ores
        options = set()
        for opt in robotOptions:
            o, r = opt 
            
            updatedOres = tuple([o[robotIndex] + robotCount for (robotIndex, robotCount) in enumerate(robots)])
            options.add((updatedOres, r))



        # append each possible new combination to the queue
        for option in options:
            o, r = option
            Q.append((o, r, minutes + 1))


    return maxGeodesMined

# ------
# PART 1
# ------

part1 = 0
for i, blueprint in enumerate(blueprints):
    part1 += bfs(blueprint, 24) * (i+1)
print(part1)

# ------
# PART 2
# ------
part2 = 1
for blueprint in blueprints[:3]:
    part2 *= bfs(blueprint, 32)
print(part2)
