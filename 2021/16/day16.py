from collections import defaultdict, deque
import re
from copy import deepcopy
import math
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt
from matplotlib import colors


with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

def binToHex(binary):
   return str(hex(int(binary, 2)))[2:]

def hexToBin(hexa):
   return bin(int(hexa, 16))[2:].zfill(4*len(hexa))

def binToDec(binary):
    if binary == '':
        return 0
    return int(binary, 2)

def addSubPacketVersionNumbers(packet):
    if packet['subPackets'] in [None, []]:
        return packet['version']
    
    count = packet['version']
    for subPacket in packet['subPackets']:
        count += addSubPacketVersionNumbers(subPacket)
    return count

def extract_next_packet(binary):
    
    packet = defaultdict(lambda: None)
    packet['version'] = binToDec(binary[:3])
    packet['ID'] = binToDec(binary[3:6])
    binary = binary[6:]

    if packet['ID'] == 4:
        encodedNumber = ""
        while True:
            # get 5 bits
            next5bits = binary[:5]
            binary = binary[5:]
            
            # add encoded part of number
            encodedNumber += next5bits[1:]

            # if first bit is 1, keep going, if 0 then break
            if next5bits[0] == '1': continue
            else: break
        
        # get rid of extra zeros and save encoded number to dict
        # 6 + len(..) is length of packet and must be a multiple of 4
        # hence we trim its modulo 4 complement
        #binary = binary[4 - (6 + len(encodedNumber))%4:]
        packet['literal'] = binToDec(encodedNumber)

    # if packet ID != 4
    else:
        # get length type ID
        packet['lengthTypeID'] = binary[0]
        binary = binary[1:]
        # init list of subpackets
        packet['subPackets'] = []

        if packet['lengthTypeID'] == '0':
            packet['subPacketBitLength'] = binToDec(binary[:15])
            binary = binary[15:]

            # iteratively get subPackets until subPacketBitLength is reached
            prevBinaryLength = len(binary)
            while prevBinaryLength - len(binary) < packet['subPacketBitLength']:
                subpacket, binary = extract_next_packet(binary)
                packet['subPackets'].append(subpacket)
        else:
            packet['numberOfSubPackets'] = binToDec(binary[:11])
            binary = binary[11:]
            # iteratively get subPackets until subPacketCount is reached
            while len(packet['subPackets']) < packet['numberOfSubPackets']:
                subpacket, binary = extract_next_packet(binary)
                packet['subPackets'].append(subpacket)

    return packet, binary

def parsePacket(packet):

    # return literal
    if packet['ID'] == 4:
        return packet['literal']

    # sum operator
    if packet['ID'] == 0:
        sum = 0        
        for subPacket in packet['subPackets']:
            sum += parsePacket(subPacket)
        return sum

    # product operator
    if packet['ID'] == 1:
        prod = 1
        for subPacket in packet['subPackets']:
            prod *= parsePacket(subPacket)            
        return prod

    # minimum operator
    if packet['ID'] == 2:
        min = np.inf
        for subPacket in packet['subPackets']:
            subPacketValue = parsePacket(subPacket)
            if subPacketValue < min:
                min = subPacketValue
        return min

    # maximum operator
    if packet['ID'] == 3:
        max = 0
        for subPacket in packet['subPackets']:
            subPacketValue = parsePacket(subPacket)
            if subPacketValue > max:
                max = subPacketValue
        return max

    # greater than operator
    if packet['ID'] == 5:
        if parsePacket(packet['subPackets'][0]) > parsePacket(packet['subPackets'][1]):
            return 1
        return 0

    # less than operator
    if packet['ID'] == 6:
        if parsePacket(packet['subPackets'][0]) < parsePacket(packet['subPackets'][1]):
            return 1
        return 0

    # equal to operator
    if packet['ID'] == 7:
        if parsePacket(packet['subPackets'][0]) == parsePacket(packet['subPackets'][1]):
            return 1
        return 0

# print out packet structure (just for visualisation)
def printSubPacket(packet, recDepth=0):
    if recDepth == 0:
        print("\n---------------------------------------------------------------------------------------")
        print("ID:ID, lit: Literal, sc: Sub-packet Count, sbl: Sub-packet bit length, version: version")
        print("---------------------------------------------------------------------------------------\n")
    if packet['subPackets'] in [None, []]:
        for _ in range(recDepth):
            print('\t', end="")
        print(f"ID:{packet['ID']}, lit:{packet['literal']}, sc:{packet['numberOfSubPackets']}, sbl:{packet['subPacketBitLength']}, version:{packet['version']}")
        return

    for _ in range(recDepth):
        print('\t', end='')
    print(f"ID:{packet['ID']}, lit:{packet['literal']}, sc:{packet['numberOfSubPackets']}, sbl:{packet['subPacketBitLength']}, version:{packet['version']}")
    for subPacket in packet['subPackets']:
        printSubPacket(subPacket, recDepth+1)

    return
    


        

############################### PART 1 ############################### 
binary = hexToBin(lines[0])
packet1, binary = extract_next_packet(binary)
print(addSubPacketVersionNumbers(packet1))
############################### PART 2 ############################### 
print(parsePacket(packet1))

printSubPacket(packet1)