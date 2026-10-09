import sys
import random

filename = sys.argv[1]
with open(filename) as f:
    for l in f:
        if random.random() <.01:
            print(l, end="")