#!/usr/bin/python

from __future__ import print_function
import sys
from collections import defaultdict

ps = defaultdict(int)

genom = sys.stdin.readline().strip()
k, d = map(int, sys.stdin.readline().strip().split())

pks = [[]]
if d > 0:
    for i in range(k):
        pks.append([i])
        if d <= 1:
            continue
        for j in range(k):
            if i >= j:
                continue
            pks.append([i, j])
            if d <= 2:
                continue
            for k in range(k):
                if j >= k:
                    continue
                pks.append([i, j, k])

G = 'ACGT'


def gen_patches(s, poses):
    if len(poses) == 0:
        return [""]
    patches = gen_patches(s, poses[1:])
    fp = poses[0]
    npatches = []
    for c in G:
        if c == s[fp]:
            continue
        for patch in patches:
            npatches.append(c + patch)
    return npatches

#~ print(gen_patches("ACGT", [0, 1, 3]))

def all_changes(s, poses):
    changes = []
    patches = gen_patches(s, poses)
    cur = [c for c in s]
    for patch in patches:
        for pos, ch in zip(poses, patch):
            cur[pos] = ch
        changes.append("".join(cur))
    return changes

for i in range(len(genom) - k + 1):
    s = genom[i:i + k]
    for pk in pks:
        for cs in all_changes(s, pk):
            ps[cs] += 1

mx = max(cc for pattern, cc in ps.items())

ans = [pattern for pattern, cc in ps.items() if cc == mx]

print(" ".join(sorted(ans)))
