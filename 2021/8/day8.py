from collections import defaultdict

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

count = 0
for line in lines:
    signal_pattern, output_pattern = line.split(" | ")
    for output in output_pattern.split(" "):
        if len(output) in [2, 4, 7, 3]:
            count += 1
print(count)


# PART 2

def sSort(signal):
    return "".join(sorted(list(signal)))

def findKey(my_dict, value):
    return list(my_dict.keys())[list(my_dict.values()).index(value)]

def letterMatchCount(s1, s2):
    count = 0
    for s in s1:
        if s in s2:
            count += 1
    return count

total_output_sum = 0
for line in lines:
    signal_pattern, output_pattern = line.split(" | ")
    signals = signal_pattern.split(" ")
    outputs = output_pattern.split(" ")

    # generate translator dict
    numberDict = defaultdict(lambda : -1)
    # find easy ones
    for signal in signals:
        if len(signal) == 2: numberDict[sSort(signal)] = 1
        if len(signal) == 4: numberDict[sSort(signal)] = 4
        if len(signal) == 3: numberDict[sSort(signal)] = 7
        if len(signal) == 7: numberDict[sSort(signal)] = 8

    # find harder ones
    for signal in signals:
        # sorted signal
        sSignal = sSort(signal)

        # dont check solved signals again
        if sSignal not in numberDict.keys():
            # either 5 2 or 3
            if len(sSignal) == 5:
                # look if 3
                if letterMatchCount(sSignal, findKey(numberDict, 1)) == 2:
                    numberDict[sSignal] = 3
                
                # look if 2
                elif letterMatchCount(sSignal, findKey(numberDict, 4)) == 2:
                    numberDict[sSignal] = 2

                # look if 5
                elif letterMatchCount(sSignal, findKey(numberDict, 4)) == 3:
                    numberDict[sSignal] = 5
            
            # either 0, 6 or 9
            if len(sSignal) == 6:
                # look if 6
                if letterMatchCount(sSignal, findKey(numberDict, 1)) == 1:
                    numberDict[sSignal] = 6
                
                # look if 0
                elif letterMatchCount(sSignal, findKey(numberDict, 4)) == 3:
                    numberDict[sSignal] = 0

                # look if 9
                elif letterMatchCount(sSignal, findKey(numberDict, 4)) == 4:
                    numberDict[sSignal] = 9

    # convert output letters to number
    total_output_sum += int("".join([str(numberDict[sSort(output)]) for output in outputs]))

print(total_output_sum)
