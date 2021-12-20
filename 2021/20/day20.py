import regex
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

alg = lines[0]

alg = regex.sub(r"\.", "0", alg)
alg = regex.sub(r"#", "1", alg)

image = np.array([[1 if c=="#" else 0 for c in l] for l in lines[2:]]) 

def pad(image, value, n=1):
    for _ in range(n):
        image = np.insert(image, len(image[0]), values=value, axis=1) # insert values before column 2
        image = np.insert(image, 0, values=value, axis=1)
        image = np.insert(image, len(image), values=value, axis=0)
        image = np.insert(image, 0, values=value, axis=0)
    return image

def process(imageIn, alg, valuesAtInfinity):

    imageOG = deepcopy(imageIn)
    imageOG = pad(imageOG, valuesAtInfinity, 1)

    outImage = deepcopy(imageOG)

    for i in range(len(imageOG)):
        for j in range(len(imageOG[0])):

            binaryImageNumber = ""
            for ii in range(-1, 2):
                for jj in range(-1, 2):

                    if (0 <= i+ii < len(imageOG)) and (0 <= j+jj < len(imageOG[0])):
                        binaryImageNumber += str(imageOG[i+ii, j+jj])
                    else:
                        binaryImageNumber += valuesAtInfinity
            outImage[i,j] = int(alg[int(binaryImageNumber, 2)])
            
    return outImage


for i in range(50):
    if alg[0] == '1':
        image = process(image, alg, str(i%2))
        if not i%2: print(i+1, "inf")
        else: print(i+1, np.count_nonzero(image==1))

    else:
        image = process(image, alg, '0')
        print(i+1, np.count_nonzero(image==1))

plt.imshow(image)
plt.savefig("output.png", dpi=300)