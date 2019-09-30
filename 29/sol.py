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

def s2uv(s):
    if s > 0:
        return [s * 2 - 2, s * 2 - 1]
    else:
        return s2uv(-s)[::-1]

def u2s(u):
    return (u / 2 + 1) * (1 - (u & 1) * 2)

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


def dist(sa, sb):
    a, b = map(ss2ps, [sa, sb])
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
    return sum(c / 2 - 1 for c in counts)


def get_step(sa, sb):
    ga, gb = map(make_g, map(ss2ps, [sa, sb]))
    h = defaultdict(list)
    for g in (ga, gb):
        for u, vs in g.items():
            for v in vs:
                h[u].append(v)

    used = set()
    for v in h:
        if v in used:
            continue
        used.add(v)
        cur_path = [v]
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
            cur_path.append(v)
        if len(cur_path) >= 4:
            cur_path = cur_path[:4]
            while cur_path[1] not in ga[cur_path[0]]:
                cur_path = cur_path[1:] + [cur_path[0]]
            return (cur_path[0], cur_path[1], cur_path[3], cur_path[2])
            print(cur_path)
            sys.exit(0)
    raise NotImplemented()

def apply_step(sa, step):
    a = ss2ps(sa)
    i, i2, j, j2 = step

    g = make_g(a)

    del_e(g, i, i2)
    del_e(g, j, j2)
    add_e(g, i, j)
    add_e(g, i2, j2)

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

    return ps2ss(make_ps(g))



sa, sb = [sys.stdin.readline().strip() for i in range(2)]
print(sa)
while dist(sa, sb) > 0:
    step = get_step(sa, sb)
    sa = apply_step(sa, step)
    print(sa)







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

