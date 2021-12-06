def valid1(pp_pair):

    occurence_count = 0

    for c in pp_pair['password']:
        if c == pp_pair['letter']:
            occurence_count += 1

    if pp_pair['min'] <= occurence_count <= pp_pair['max']:
        return True

    else:
        return False

def valid2(pp):
    
    # ^ is binary xor operator
    if (pp['password'][pp['min']-1] == pp['letter']) ^ (pp['password'][pp['max']-1] == pp['letter']):
        return True
    else:
        return False

with open("input.dat", 'r') as file:
    lines = file.readlines()

    valid1_count = 0
    valid2_count = 0
    for line in lines:
        line = line.strip()

        # get data from file put into dict
        pp_pair = { 'min' : int(line[:line.index('-')]),
                    'max' : int(line[line.index('-') + 1:line.index(' ')]),
                    'letter' : line[line.index(' ') + 1:line.index(':')],
                    'password' : line[line.index(':') + 2:]}

        if valid1(pp_pair):
            valid1_count += 1 
        if valid2(pp_pair):
            valid2_count += 1
        
print("Part1: ", valid1_count)
print("Part2: ", valid2_count)