from numpy.core.fromnumeric import sort

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]


count  = 0
biggest = 0
for line in lines:
    if line == "":
        count = 0
        continue
    
    count += int(line)
    if count > biggest:
        biggest = count
    
print(biggest)

# --- PART 2

elfList = []

count  = 0
biggest = 0
for i, line in enumerate(lines):
    if line == "" or i == len(lines)-1:
        elfList.append(count)
        count = 0
        continue
    
    count += int(line)
    if count > biggest:
        biggest = count

print(sum(sort(elfList)[-3:]))