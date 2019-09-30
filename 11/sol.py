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

k = int(sys.stdin.readline().strip())
kmers = list(map(A, map(str.strip, sys.stdin)))
n = len(kmers)

in_deg = defaultdict(int)
g = defaultdict(lambda: defaultdict(int))
for kmer in kmers:
    g[S(kmer[:-1])][S(kmer[1:])] += 1
    g[S(kmer[1:])] # touch
    in_deg[S(kmer[1:])] += 1
    in_deg[S(kmer[:-1])] # touch


#~ print(g)
#~ print(in_deg)

def find_src():
    for v in g:
        if sum(g[v].values()) > in_deg[v]:
            return v
    assert False

src = find_src()

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

print(ss)




#~ print(k, kmers)


