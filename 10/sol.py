#!/usr/bin/python

from __future__ import print_function
import sys
from collections import defaultdict
import numpy as np
npa = np.array
from tqdm import tqdm
import random
import copy
import time

# previous solutions was very slow :(
# try to fasten with numpy

mers = "ATCG"
mers_a = np.fromstring(mers, np.int8)
c2n = np.zeros(255, dtype=np.int8)
c2n[mers_a] = np.arange(len(mers))

def S(a):
    return mers_a[a].tostring()

def A(s):
    return c2n[np.fromstring(s, np.int8)]


assert S(A("ATCGAAATTTCCCGGG")) == "ATCGAAATTTCCCGGG"


def hd(a, b):
    return (a != b).sum()

pattern = A(sys.stdin.readline().strip())
dna = list(map(A, map(str.strip, sys.stdin.readline().split())))

k = len(pattern)

result = 0
for s in dna:
    L = len(s)
    result += min(hd(pattern, s[i:i+k]) for i in range(L - k + 1))

print(result)


