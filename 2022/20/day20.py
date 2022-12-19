with open('input.dat', 'r') as file:
    lines = [int(line.strip()) for line in file.readlines()]


def mix(input, totalMixCount, decryptionKey = 1):

    sequence = []
    for i, x in enumerate(input):
        sequence.append((x * decryptionKey, i))

    # loop over len of sequence
    for _ in range(totalMixCount):
        for ogIndexOfItemToBeMoved in range(len(sequence)):
            
            # find the first element that has not been moved yet
            initialIndex = 0
            for i in range(len(sequence)):
                if sequence[i][1] == ogIndexOfItemToBeMoved:
                    initialIndex = i
                    break
            
            # remove form sequence
            movedItem = sequence.pop(initialIndex)

            # calc new index
            newIndex = (initialIndex + movedItem[0]) % len(sequence)

            # when items move backwards and end at the start, they should wrap to the back
            if movedItem[0] != 0 and newIndex == 0:
                newIndex = len(sequence)
            

            # insert back into sequence
            sequence.insert(newIndex, movedItem)
        
    return [i for i,_ in sequence]

def calcAnswer(sequence):

    answer = 0
    index0 = sequence.index(0)
    for x in [1_000, 2_000, 3_000]:
        answer += sequence[(index0 + x) % len(sequence)]
    return answer

print(calcAnswer(mix(lines, 1)))
print(calcAnswer(mix(lines, 10, 811589153)))
