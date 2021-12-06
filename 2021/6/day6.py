   
with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

initial = list(map(int,lines[0].split(",")))

'''
array = np.array(initial, dtype=int)
def oneday(array):
    newcount = 0
    for i,a in enumerate(array):
        
        if a == 0:
            array[i] = 6
            newcount += 1
        else:
            array[i] -= 1

    return np.append(array, np.array([8 for _ in range(newcount)], dtype=int))
'''

# convert to count of how many fish are at particular days
Darray = {}
for a in initial:
    if a not in Darray:
        Darray[a] = 0

    Darray[a] += 1

for i in range(256):
    # newdict for every day
    nDarray = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    # loop through dict
    for a, n in Darray.items():
        # if internal clock is 0, then n fish are reset to 6 and n new fish are created with 8
        if a==0:
            nDarray[6] += n
            nDarray[8] += n
        
        # all other fish reduce their clocks by 1 
        else:
            nDarray[a-1] += n

    Darray = nDarray

    if i == 80:
        print("Part1: ", sum(Darray.values()))
   

print("Part2: ", sum(Darray.values()))