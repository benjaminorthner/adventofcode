import sys
import numpy
import matplotlib.pyplot as plt

def gen_public_key(subject_number, loop_size):

    value = 1

    for i in range(loop_size):
        value *= subject_number
        value = value % 20201227

    return value

def find_loop_size(subject_number, p_keys_to_find):

    value = 1

    # loop the max number of times

    for loop_size in range(20201227):
        value = (value*subject_number) % 20201227

        # check if value matches key to find
        if value in p_keys_to_find:
            return loop_size + 1

print(find_loop_size(7, [10212254, 12577395]))
print(gen_public_key(12577395, 1063911))
