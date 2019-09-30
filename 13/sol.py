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

k, d = map(int, sys.stdin.readline().strip().split())
kmers = list(map(str.strip, sys.stdin))
kmersA = [[A(s.split('|')[i]) for s in kmers] for i in range(2)]
n = len(kmers)

def unite(kmers, kmersH):
    in_deg = defaultdict(int)
    g = defaultdict(lambda: defaultdict(int))
    for kmer, kmerH in zip(kmers, kmersH):
        u = S(kmer[:-1]) + '|' + S(kmerH[:-1])
        v = S(kmer[1:]) + '|' + S(kmerH[1:])
        g[u][v] += 1
        g[v] # touch
        in_deg[v] += 1
        in_deg[u] # touch


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
        vs = list(g[v])
        np.random.shuffle(vs)
        for u in vs:
            while gc[v][u] > 0:
                gc[v][u] -= 1
                find_euler_path(u)
        path.append(v)

    find_euler_path(src)

    path = list(reversed(path))
    path = [p.split('|')[0] for p in path]

    def glue_path(path):
        res = [path[0]]
        for p in path[1:]:
            res.append(p[-1])
        return "".join(res)

    #~ print(src)
    #~ print(path)

    ss = glue_path(path)

    return ss

for i in tqdm(range(100500)):
    a = unite(kmersA[0], kmersA[1])
    b = unite(kmersA[1], kmersA[0])
    if a[k+d:] == b[:-(k+d)]:
        print(a[:k+d] + b)
        break

#~ print(unite(kmersA[0]))
#~ print(unite(kmersA[1]))



#~ print(k, kmers)


