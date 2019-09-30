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

p = list(map(int, sys.stdin.readline().strip()[1:-1].split()))


def pretty(p):
    return "(%s)" % " ".join("%+d" % i for i in p)

for i in range(len(p)):
    if abs(p[i]) != i + 1:
        j = next(j for j in range(i + 1, len(p)) if abs(p[j]) == i + 1)
        p[i:j+1] = [-x for x in p[i:j+1][::-1]]
        print(pretty(p))
    if p[i] == -(i + 1):
        p[i] = i + 1
        print(pretty(p))

