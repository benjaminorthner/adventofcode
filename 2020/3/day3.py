def count_trees(map, rule):
    map_height = len(map)
    map_width = len(map[0])

    # start coordinates
    x = 0
    y = 0
    tree_count = 0

    # step through map until bottom is reached
    while y < map_height:
        if map[y][x % map_width] == '#':
            tree_count += 1
        
        # make a step based on rule
        x += rule[0]
        y += rule[1]

    return tree_count


# import tree map
with open("input.dat", 'r') as file:
    lines = file.readlines()

    map = []
    for line in lines:
        map.append(line.strip())

# [steps right, steps down]
rules = [[1, 1],
         [3, 1],
         [5, 1],
         [7, 1],
         [1, 2]]

tree_count_prod = 1
for rule in rules:
    tree_count_prod *= count_trees(map, rule)

print(tree_count_prod)
    

