# Parse the input and store it in a list of pairs
pairs = []
with open('input.txt') as f:
  for line in f:
    assignments = line.strip().split(',')
    group = []
    for assignment in assignments:
      a, b = map(int, assignment.split('-'))
      group.append((a,b))
    pairs.append(group)

# Count the number of pairs where one range fully contains the other
count = 0
for (a1, b1), (a2, b2) in pairs:
  # Check if the first range fully contains the second range
  if a1 <= a2 and b1 >= b2:
    count += 1
  # Check if the second range fully contains the first range
  elif a2 <= a1 and b2 >= b1:
    count += 1

# Print the result
print(count)

# Count the number of pairs where the ranges overlap
count = 0
for (a1, b1), (a2, b2) in pairs:
  # Check if the first range overlaps the second range
  if (a1 <= b2 and b1 >= b2) or (b1 >= a2 and b1 <= b2):
    count += 1
  # Check if the second range overlaps the first range
  elif (a2 <= b1 and b2 >= b1) or (b2 >= a1 and b2 <= b1):
    count += 1

# Print the result
print(count)