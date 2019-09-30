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
        for j in range(i + 1, k):
            pks.append([i, j])
            if d <= 2:
                continue
            for l in range(j + 1, k):
                pks.append([i, j, l])

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

#~ print(gen_patches("ACGT", [0]))
#~ print(gen_patches("ACGT", [0, 3]))
#~ print(gen_patches("ACGT", [0, 1, 3]))

def all_changes(s, poses):
    changes = []
    patches = gen_patches(s, poses)
    cur = [c for c in s]
    for patch in patches:
        for pos, ch in zip(poses, patch):
            cur[pos] = ch
        ss = "".join(cur)
        assert sum(a != b for a, b in zip(s, ss)) == len(poses)
        changes.append(ss)
    return changes

COM = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C',
}

def revcom(s):
    return "".join(COM[c] for c in s[::-1])

for i in range(len(genom) - k + 1):
    s = genom[i:i + k]
    for pk in pks:
        for cs in all_changes(s, pk):
            cse = revcom(cs)
            #if cs < cse:
            ps[cs] += 1
            #else:
            ps[cse] += 1

mx = max(cc for pattern, cc in ps.items())

ans = [pattern for pattern, cc in ps.items() if cc == mx]

print(" ".join(sorted(ans)))

#~ print(list(sorted(ps.items(), key=lambda x: x[0])))

# ACGTTGCATGTCGCATGATGCATGAGAGCT
# ACAT ACAT   ACAT   ACAT
#     TACA          TACA

#~ ACAT 4
#~ TACA 2


# ACGTTGCATGTCGCATGATGCATGAGAGCT
# ATGT   ATGT   ATGT   ATGT
#                  ATGT
#     TGTATGTA      TGTA

#~ ATGT 5
#~ TGTA 3
