import numpy as np

with open("input.dat", "r") as file:
    lines = [list(map(int,list(line.strip()))) for line in file.readlines()]

def flash(oMap):
    oMap += 1

    while (oMap > 9).any():
        for i in range(len(oMap)):
            for j in range(len(oMap[0])):
                if oMap[i,j] > 9:
                    
                    # set the flashed one to 0 and increment its neighbours (that are not 0 themselves)
                    oMap[i,j] = 0
                    for ii in range(-1, 2):
                        for jj in range(-1, 2):
                            if (0 <= i+ii < len(oMap)) and (0 <= j+jj < len(oMap[0])):
                                if oMap[i+ii, j+jj] != 0:
                                    oMap[i+ii, j+jj] += 1

# PART 1
oMap = np.array(lines, dtype=int)
flash_counter = 0
for i in range(100):
    flash(oMap)
    flash_counter += np.count_nonzero(oMap == 0)
print(flash_counter)

# PART 2
oMap = np.array(lines, dtype=int)
i = 0
while True:
    i+=1
    flash(oMap)
    if (oMap == 0).all():
        break
print(i)

