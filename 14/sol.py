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

#k, d = map(int, sys.stdin.readline().strip().split())
kmers = list(map(str.strip, sys.stdin))
#kmersA = [[A(s.split('|')[i]) for s in kmers] for i in range(2)]
n = len(kmers)

#~ print(kmers)

in_deg = defaultdict(int)
g = defaultdict(lambda: defaultdict(int))
for kmer in kmers:
    u = kmer[:-1]
    v = kmer[1:]
    g[u][v] += 1
    g[v] # touch
    in_deg[v] += 1
    in_deg[u] # touch


#~ print(g)
#~ print(in_deg)

#~ def find_src():
    #~ for v in g:
        #~ if sum(g[v].values()) > in_deg[v]:
            #~ return v
    #~ assert False

#~ src = find_src()

def glue_path(path):
    res = [path[0]]
    for p in path[1:]:
        res.append(p[-1])
    return "".join(res)



next_E = {}
prev_E = {}
#~ in_deg_E = defaultdict(int)
count_E = defaultdict(int)

for v in g.keys():
    for u in g[v]:
        for z in range(g[v][u]):
            e1 = v + u[-1]
            count_E[e1] += 1
            #~ next_E[e1]

            if sum(g[u].values()) == 1 and in_deg[u] == 1:
                e2 = u + list(g[u])[0][-1]
                #~ in_deg_E[e2] += 1
                #~ next_E[e2]
                next_E[e1] = e2
                prev_E[e2] = e1


def unlim(e):
    for i in range(len(next_E) * 2):
        if e not in prev_E:
            return False
        e = prev_E[e]
    return True

#~ print(next_E)
#~ print(prev_E)
#~ print(count_E)

resS = []
for e1 in count_E:
    es = e1
    if e1 in prev_E and not unlim(e1):
        continue
    assert count_E[e1] == 1 or (e1 not in prev_E and e1 not in next_E)

    if count_E[e1] == 1:
        path = [e1]
        if e1 in next_E and next_E[e1] == e1:
            pass
        else:
            if e1 in next_E:
                e2 = next_E[e1]
                path.append(e2)
                while e2 in next_E and next_E[e2] != e1:
                    e2 = next_E[e2]
                    path.append(e2)
        resS.append(glue_path(path))
    else:
        for i in range(count_E[e1]):
            resS.append(e1)



print(" ".join(sorted(resS)))


#~ print(unite(kmersA[0]))
#~ print(unite(kmersA[1]))



#~ print(k, kmers)


