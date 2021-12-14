from collections import defaultdict, deque
import re
from copy import deepcopy
import math
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]