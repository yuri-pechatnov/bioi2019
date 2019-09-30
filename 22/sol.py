#!/usr/bin/python

from __future__ import print_function
import sys
from collections import defaultdict, Counter
import numpy as np
npa = np.array
from tqdm import tqdm
import random
from copy import copy
import time
import sys

sys.setrecursionlimit(100000)

#~ 4 4
#~ 1 0 2 4 3
#~ 4 6 5 2 1
#~ 4 4 5 2 1
#~ 5 6 8 5 3
#~ -
#~ 3 2 4 0
#~ 3 2 4 2
#~ 0 7 3 3
#~ 3 3 0 2
#~ 1 3 2 2

n, m = map(int, sys.stdin.readline().strip().split())
up = [list(map(int, sys.stdin.readline().strip().split())) for i in range(n)]
assert sys.stdin.readline().strip() == '-'
right = [list(map(int, sys.stdin.readline().strip().split())) for i in range(n + 1)]

#~ print(n, m)
#~ print(up)
#~ print(right)

d = defaultdict(lambda: -1e100, {(0, 0): 0})

def G(arr, i, j):
    if i < 0 or j < 0:
        return -1e100
    return arr[i][j]

for i in range(n + 1):
    for j in range(m + 1):
        if i == j == 0:
            continue
        d[(i, j)] = max(
            d[(i - 1, j)] + G(up, i - 1, j),
            d[(i, j - 1)] + G(right, i, j - 1),
        )

print(d[(n, m)])
