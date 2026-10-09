import sys
import random

filename = sys.argv[1]
with open(filename) as py:
    for line in py:
        if random.random() <.01:
            print(line, end="")
