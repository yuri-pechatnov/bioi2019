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

def ss2ps(s):
    return list(map(lambda p: [int(x) for x in p.split()], s.strip()[1:-1].split(')(')))

def ps2ss(ps):
    return "".join("(%s)" % " ".join("%+d" % x for x in p) for p in ps)

a = ss2ps(sys.stdin.readline())
i, i2, j, j2 = [int(x) - 1 for x in sys.stdin.readline().strip().split(',')]

def s2uv(s):
    if s > 0:
        return [s * 2 - 2, s * 2 - 1]
    else:
        return s2uv(-s)[::-1]

def u2s(u):
    return (u / 2 + 1) * (1 - (u & 1) * 2)

#~ print(s2uv(1))
#~ print(s2uv(-1))


def add_e(g, u, v):
    g[u].append(v)
    g[v].append(u)


def del_e(g, u, v):
    g[u] = [x for x in g[u] if x != v]
    g[v] = [x for x in g[v] if x != u]


def make_g(ps):
    g = defaultdict(list)
    for p in ps:
        for i in range(len(p)):
            u = s2uv(p[i - 1])[1]
            v = s2uv(p[i])[0]
            add_e(g, u, v)
    return g

g = make_g(a)

print(g)

del_e(g, i, i2)
del_e(g, j, j2)
add_e(g, i, j)
add_e(g, i2, j2)

print(g)

def make_ps(g):
    used = set()

    ps = []

    for v in g:
        if v in used:
            continue
        used_l = []
        used.add(v)
        used_l.append(v)
        v = v ^ 1
        used.add(v)
        used_l.append(v)

        while True:
            nv = None
            for u in g[v]:
                if u not in used:
                    nv = u
                    break
            if nv is None:
                break
            v = nv
            used.add(v)
            used_l.append(v)
            v = v ^ 1
            used.add(v)
            used_l.append(v)
        ps.append(list(map(u2s, used_l[::2])))
    return ps


print(make_ps(g))

print(ps2ss(make_ps(g)))

print(i, i2, j, j2)


#~ counts = []

#~ used = set()

#~ for v in h:
    #~ if v in used:
        #~ continue
    #~ used.add(v)
    #~ cur_cnt = 1
    #~ while True:
        #~ nv = None
        #~ for u in h[v]:
            #~ if u not in used:
                #~ nv = u
                #~ break
        #~ if nv is None:
            #~ break
        #~ v = nv
        #~ used.add(v)
        #~ cur_cnt += 1
    #~ counts.append(cur_cnt)

#~ ans = sum(c / 2 - 1 for c in counts)

#~ print(ans)

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

