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

a, b = [list(map(lambda p: [int(x) for x in p.split()], sys.stdin.readline().strip()[1:-1].split(')('))) for i in range(2)]

def s2uv(s):
    if s > 0:
        return [s * 2 - 2, s * 2 - 1]
    else:
        return s2uv(-s)[::-1]

#~ print(s2uv(1))
#~ print(s2uv(-1))


def make_g(ps):
    g = defaultdict(list)
    for p in ps:
        for i in range(len(p)):
            u = s2uv(p[i - 1])[1]
            v = s2uv(p[i])[0]
            g[u].append(v)
            g[v].append(u)
    return g


h = defaultdict(list)

for x in (a, b):
    g = make_g(x)
    for u, vs in g.items():
        for v in vs:
            h[u].append(v)

counts = []

used = set()

for v in h:
    if v in used:
        continue
    used.add(v)
    cur_cnt = 1
    while True:
        nv = None
        for u in h[v]:
            if u not in used:
                nv = u
                break
        if nv is None:
            break
        v = nv
        used.add(v)
        cur_cnt += 1
    counts.append(cur_cnt)

ans = sum(c / 2 - 1 for c in counts)

print(ans)

#~ tt = defaultdict(int)

#~ for x in (a, b):
    #~ g = make_g(x)
    #~ for u, vs in g.items():
        #~ for v in vs:
            #~ tt[(u, v)] ^= 1

#~ print(sum(tt.values()) / 4)

#~ print(counts)

#~ print(a, b)

#print(list( zip(p[:-1], p[1:])))
#~ def pretty(p):
    #~ return "(%s)" % " ".join("%+d" % i for i in p)

