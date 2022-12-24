with open('input.dat', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

symbols = ['=', '-', '0', '1', '2']

def toDecimal(SNAFU):
    return sum([5 ** i *(symbols.index(digit) - 2) for i, digit in enumerate(reversed(SNAFU))])

def toSNAFU(n):
    s = ""
    while n:
        s = symbols[(n + 2) % 5] + s
        if n + 2 >= 5:
            n += 2 # add back the part lost in taking the modulo
        n //= 5
    return s

print(toSNAFU(sum([toDecimal(SNAFU) for SNAFU in lines])))