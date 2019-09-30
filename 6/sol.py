#!/usr/bin/python

from __future__ import print_function
import sys
from collections import defaultdict
import numpy as np
npa = np.array
import tqdm


ps = defaultdict(int)


k, t = map(int, sys.stdin.readline().strip().split())
genom = [sys.stdin.readline().strip() for i in range(t)]

toi = {
    'A': 0,
    'T': 1,
    'G': 2,
    'C': 3,
}


def extract(ix):
    return [genom[o][i:i+k] for o, i in enumerate(ix)]

def score(ix):
    ss = extract(ix)
    #print(ss)
    m = npa([list(map(toi.get, s)) for s in ss])

    #print(m)
    cc = np.zeros((m.shape[1], len(toi)))
    for mi in m:
        #~ print(cc.shape, [np.arange(len(toi)), mi])
        cc[[np.arange(m.shape[1]), mi]] += 1
    #~ print(cc)
    c = cc.argmax(axis=1)
    #~ print(c)

    #~ print(m != c)
    res = (m != c).sum()

    #~ print(res)
    #~ print(ss)
    #~ print(np.array([list(map(toi.get, s)) for s in ss]))
    return res

def find_profile(ix):
    ss = extract(ix)
    #print(ss)
    m = npa([list(map(toi.get, s)) for s in ss])

    #print(m)
    cc = np.zeros((m.shape[1], len(toi)))
    for mi in m:
        #~ print(cc.shape, [np.arange(len(toi)), mi])
        cc[[np.arange(m.shape[1]), mi]] += 1
    cc = cc.astype(float) / len(ix)
    #print(cc)
    return cc

def appro(p, s):
    s = npa(list(map(toi.get, s)))
    #print(s)
    #print(p)
    #print([np.arange(len(s)), s])
    return np.prod(p[[np.arange(len(s)), s]])

L = len(genom[0]) - k + 1
bestm = [0] * t

for fpos in tqdm.tqdm(range(L)):
    curm = [fpos]
    for i in range(1, len(genom)):
        profile = find_profile(curm)
        bj = 0
        ibestm = curm + [bj]
        bs = appro(profile, genom[i][:k])
        for j in range(1, L):
            icurm = curm + [j]
            ics = appro(profile, genom[i][j:j+k])
            if ics > bs:
                ibestm = icurm
                bj = j
                bs = ics
        curm.append(bj)
    if score(curm) < score(bestm):
        bestm = curm

print(bestm)
print(score(bestm))
print("\n".join(extract(bestm)))


print(score([0, 1]))

