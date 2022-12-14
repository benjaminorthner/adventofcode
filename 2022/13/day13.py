from ast import literal_eval
from functools import cmp_to_key

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]
    pairs = [(literal_eval(p1), literal_eval(p2)) for p1, p2 in zip(lines[::3], lines[1::3])]

# ------
# PART 1
# ------

def checkOrder(pL, pR):
    for (L, R) in zip(pL, pR):
        # if both int
        if isinstance(L, int) and isinstance(R, int):
            if L < R: return True
            elif L > R: return False
            else: continue
        
        # if mixed list and int
        if isinstance(L, int):
            L = [L]
        else:
            R = [R]

        # if both lists
        if isinstance(L, list) and isinstance(R, list):
            listCheckReturn = checkOrder(L, R)

            if listCheckReturn == None: continue
            else: return listCheckReturn
        

    if len(pL) < len(pR): return True
    elif len(pL) > len(pR): return False


print(sum([i * checkOrder(pL, pR) for i, (pL, pR) in enumerate(pairs, start=1)]))


# ------
# PART 2
# ------

# remove gaps and make packet list (with dividers)
del lines[2::3]
packets = [literal_eval(line) for line in lines]
packets.append([[2]])
packets.append([[6]])

# run the sort
packets = sorted(packets, key=cmp_to_key(lambda a,b: -1 if checkOrder(a,b) else 1))

# print result
pi1 = packets.index([[2]]) + 1
pi2 = packets.index([[6]]) + 1

print(pi1 * pi2)

for p in packets:
    break
    print(p)

print(checkOrder([[6]], [6, 0, 1, 5]))