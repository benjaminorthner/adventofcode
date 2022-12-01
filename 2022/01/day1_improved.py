with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

Q = []
for elf in "\n".join(lines).split('\n\n'):
    count = 0
    for cal in elf.split('\n'):
        count += int(cal)
    Q.append(count)

Q = sorted(Q)
print(Q[-1])
print(sum(Q[-3:]))