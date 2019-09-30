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
import sys

sys.setrecursionlimit(100000)

# previous solutions was very slow :(
# try to fasten with numpy

mers = "01ATCG"
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

def all_bin(k):
    res = []
    for i in range(1 << k):
        res.append(np.fromstring(("0" * k + bin(i)[2:])[-k:], np.int8) - ord('0'))
    return res


k = int(sys.stdin.readline().strip())
kmers = all_bin(k)
n = len(kmers)

print(kmers)

in_deg = defaultdict(int)
g = defaultdict(lambda: defaultdict(int))
for kmer in kmers:
    g[S(kmer[:-1])][S(kmer[1:])] += 1
    g[S(kmer[1:])] # touch
    in_deg[S(kmer[1:])] += 1
    in_deg[S(kmer[:-1])] # touch


#~ print(g)
#~ print(in_deg)

src = S(kmers[0][:-1])

gc = copy.copy(g)
path = []
def find_euler_path(v):
    for u in g[v]:
        while gc[v][u] > 0:
            gc[v][u] -= 1
            find_euler_path(u)
    path.append(v)

find_euler_path(src)

path = list(reversed(path))

def glue_path(path):
    res = [path[0]]
    for p in path[1:]:
        res.append(p[-1])
    return "".join(res)

#~ print(src)
#~ print(path)

ss = glue_path(path)

print(ss[:-k + 1])




#~ print(k, kmers)


