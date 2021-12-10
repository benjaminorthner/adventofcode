import re
import numpy as np

with open("input.dat", 'r') as file:
    lines = [line for line in file.readlines()]

array = []
for line in lines:
    array.append(re.findall("\d+", line)[0])

gammarate = []
epsilonrate= []
for i in range(len(array[0])):
    count0=0
    count1=0
    for j in range(len(array)):
        if array[j][i] == '0':
            count0 += 1
        else:
            count1 += 1
    
    if count1 > count0:
        gammarate.append(1)
        epsilonrate.append(0)

    else:
        gammarate.append(0)
        epsilonrate.append(1)

gamma=sum([val*2**(11-i) for i, val in enumerate(gammarate)])
epsilon=sum([val*2**(11-i) for i, val in enumerate(epsilonrate)])

print(gamma*epsilon)


def mostcommonbit(array, col):
    
    c1=0
    c0=0
    for bit in array[:,col]:
        if bit ==1:
            c1 +=1
        elif bit ==0:
            c0+=1

    if c1 >= c0:
        return 1
    
    return 0


def leastcommonbit(array, col):
        
    c1=0
    c0=0
    for bit in array[:,col]:
        if bit ==1:
            c1 +=1
        elif bit ==0:
            c0+=1

    if c0 <= c1:
        return 0
    
    return 1


array = []
for line in lines:
    line.strip()
    array.append(np.array(list(map(int,re.findall("\d", line)))))

array2 = np.array(array)
array3 = np.array(array)

for col in range(len(array2[0])):

    mcb = mostcommonbit(array2, col)

    loop = True
    row = 0
    while loop:
        if row == len(array2):
            break

        if array2[row, col] != mcb:
            array2 = np.delete(array2, row, 0)
        else:
            row +=1
    

for col in range(len(array3[0])):

    lcb = leastcommonbit(array3, col)

    loop = True
    row = 0
    while loop:
        if row == len(array3):
            break

        if len(array3) == 1:
            break

        if array3[row, col] != lcb:
            array3 = np.delete(array3, row, 0)
        else:
            row +=1
    
    if len(array3) == 1:
        break

oxygen = sum([val*2**(11-i) for i, val in enumerate(array2[0])])
co2 = sum([val*2**(11-i) for i, val in enumerate(array3[0])])

print(oxygen*co2)