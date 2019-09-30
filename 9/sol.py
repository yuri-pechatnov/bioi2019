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

ps = defaultdict(int)


k, t, N = map(int, sys.stdin.readline().strip().split())
genom = [sys.stdin.readline().strip() for i in range(t)]

toi = {
    'A': 0,
    'T': 1,
    'G': 2,
    'C': 3,
}


def extract(ix):
    if isinstance(ix[0], tuple):
        return [genom[o][i:i+k] for o, i in ix]
    else:
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
    sigma = 0.8
    cc = np.ones((m.shape[1], len(toi))) * sigma
    for mi in m:
        #~ print(cc.shape, [np.arange(len(toi)), mi])
        cc[[np.arange(m.shape[1]), mi]] += 1
    cc = cc.astype(float) / (len(ix) + sigma * len(toi))
    #print(cc)
    return cc

def appro(p, s):
    s = npa(list(map(toi.get, s)))
    #print(s)
    #print(p)
    #print([np.arange(len(s)), s])
    return np.prod(p[[np.arange(len(s)), s]])





L = len(genom[0]) - k + 1

def rskm():
    return [random.randrange(L) for g in genom]

def mafpi(g, profile):
    bj = 0
    bs = appro(profile, g[:k])
    for j in range(1, L):
        ics = appro(profile, g[j:j+k])
        if ics > bs:
            bj = j
            bs = ics
    return bj

def mafp(profile):
    return [mafpi(g, profile) for g in genom]

def mafp2(g, profile):
    pp = npa([appro(profile, g[i:i+k]) for i in range(L)])
    pp /= pp.sum()
    return int(np.random.choice(np.arange(L), 1, p=pp))


def rms():
    oldm = rskm()
    soldm = score(oldm)
    while True:
        profile = find_profile(oldm)
        nowm = mafp(profile)
        snowm = score(nowm)
        if snowm < soldm:
            #print("hit")
            soldm = snowm
            oldm = nowm
        else:
            return oldm

def gs():
    oldm = rskm()
    soldm = score(oldm)
    for j in range(N):
        i = random.randrange(len(genom))
        profile = find_profile([(ip, p) for ip, p in enumerate(oldm) if ip != i])
        ns = mafp2(genom[i], profile)
        nowm = copy.copy(oldm)
        nowm[i] = ns
        snowm = score(nowm)
        if snowm < soldm:
            #print("hit")
            soldm = snowm
            oldm = nowm
    return oldm


bestm = rskm()
stime = time.time()
#~ while (time.time() - stime) < 60 * 4:
for i in tqdm(range(20)):
    curm = gs()
    if score(curm) < score(bestm):
        bestm = curm


print(bestm)
print(score(bestm))
print("\n".join(extract(bestm)))



