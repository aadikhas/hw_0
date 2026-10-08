import sys
import random

filename = sys.argv[1]
with open(filename) as file:
    for line in file:
        if random.random() <.01:
            print(line, end="")
