from math import prod

with open("input.dat", 'r') as file:
    lines = [line.strip() for line in file.readlines()]

class Monkey:

    def __init__(self, monkeyNumber) -> None:
        self.monkeyNumber = monkeyNumber
        self.items = []
        self.inspectionCount = 0

        self.operand = None
        self.operator = None

        self.modulo = None
        self.ifTrue = None
        self.ifFalse = None
    	
    def operation(self, old):
        if self.operand == 'old':
            if self.operator == "*":
                return old ** 2 
            else:
                return 2 * old

        elif self.operator == "*":
            return old * int(self.operand)
        else:
            return old + int(self.operand)
    
    def test(self, toBeTested):
        if toBeTested % self.modulo == 0:
            return self.ifTrue
        return self.ifFalse


# PARSE INPUT
def LoadMonkeys():

    monkeylist = []
    for line in lines:
        if line != "":
            label, *[values] = line.split(":")

            if "Monkey" in label:
                _, monkeyNumber = label.split(" ")
                monkeylist.append(Monkey(monkeyNumber))
            
            elif "Starting items" in label:
                monkeylist[-1].items = [int(i.strip()) for i in values.split(",")]

            elif "Operation" in label:
                monkeylist[-1].operator = values.split(" ")[-2]
                monkeylist[-1].operand = values.split(" ")[-1]
    
            elif "Test" in label:
                monkeylist[-1].modulo = int(values.split(" ")[-1])
            
            elif "If true" in label:
                monkeylist[-1].ifTrue = int(values.split(" ")[-1])

            elif "If false" in label:
                monkeylist[-1].ifFalse = int(values.split(" ")[-1])
    return monkeylist

monkeylist = LoadMonkeys()


# -----------
# PART 2
# -----------


# PERFORM THE ROUNDS
for _ in range(20):
    for monkey in monkeylist:
        for item in monkey.items:
            monkey.inspectionCount += 1
            new = monkey.operation(item) // 3
            monkeylist[monkey.test(new)].items.append(new)
            
        monkey.items = []

print(prod(sorted([monkey.inspectionCount for monkey in monkeylist])[-2:]))


# -----------
# PART 2
# -----------

monkeylist = LoadMonkeys()

# PERFORM THE ROUNDS
mod = prod([m.modulo for m in monkeylist])
for i in range(10000):
    for monkey in monkeylist:
        for item in monkey.items:
            monkey.inspectionCount += 1
            new = monkey.operation(item) % mod # does not affect which monkey receives item, but keeps numbers low 
            monkeylist[monkey.test(new)].items.append(new)
            
        monkey.items = []

print(prod(sorted([monkey.inspectionCount for monkey in monkeylist])[-2:]))