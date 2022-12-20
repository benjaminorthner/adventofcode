with open("input.dat", 'r') as file:
    lines = [line.strip() for line in file.readlines()]


monkeys = {}
for line in lines:
    name, operation = line.split(": ")
    try:
        operation = int(operation)
    except:
        pass
    monkeys[name] = operation
    
def evaluateMonkey(name):
    operation = monkeys[name]

    if isinstance(operation, int):
        return operation

    m1, op, m2 = operation.split(" ")
    return eval(f"{evaluateMonkey(m1)} {op} {evaluateMonkey(m2)}")

print(int(evaluateMonkey('root')))

# -------
# PART 2
# -------

# change roots operation to be subtractive (to use root finding technique)
m1, op, m2 = monkeys['root'].split(" ")
monkeys['root'] = f"{m1} - {m2}"

# NEWTON-RAPHSON method
def f(humn):
    monkeys['humn'] = humn
    return evaluateMonkey('root')

def df(humn):
    f1 = f(humn)
    f2 = f(humn + 1)

    return f2 - f1

humn = 4400
while f(humn) != 0:
    humn = int(humn - f(humn) / df(humn))

print(humn)
