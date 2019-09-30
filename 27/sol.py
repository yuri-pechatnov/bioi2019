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
print(sum((a + 1 != b) for a, b in zip([0] + p, p + [len(p) + 1])))

#print(list( zip(p[:-1], p[1:])))
#~ def pretty(p):
    #~ return "(%s)" % " ".join("%+d" % i for i in p)

