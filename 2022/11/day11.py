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




for rounds, function in zip([20, 10000], [lambda x, _: x // 3, lambda x, mod: x % mod]):

    # Load fresh set of monkey
    monkeylist = LoadMonkeys()

    # needed for part 2. After calculating the "new" value we take its modulo
    # with respect to a number that is divisible by all monkeys modulo number
    # this does not affect which monkey receives the item, but keeps the actual 
    # numbers low and thus prevents the code from slowing down over time.s
    mod = prod([m.modulo for m in monkeylist])

    # Perform the rounds
    for _ in range(rounds):
        for monkey in monkeylist:
            for item in monkey.items:
                monkey.inspectionCount += 1
                new = function(monkey.operation(item), mod)
                monkeylist[monkey.test(new)].items.append(new)
                
            monkey.items = []

    # print product of two highest inspection counts
    print(prod(sorted([monkey.inspectionCount for monkey in monkeylist])[-2:]))