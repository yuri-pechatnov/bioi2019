#!/usr/bin/python

from __future__ import print_function
import sys
from collections import defaultdict

genom = sys.stdin.readline().strip()
k, L, t = map(int, sys.stdin.readline().strip().split())

seqs = [genom[i:i + k] for i in range(0, len(genom) - k + 1)]
L = L - k + 1

if L <= 0:
    sys.exit(0)

poses = defaultdict(list)

for pos, seq in enumerate(seqs):
    poses[seq].append(pos)

ans = []

def decide(poses, L, t):
    for i in range(0, len(poses) - t + 1):
        if poses[i + t - 1] - poses[i] < L:
            return True
    return False

for seq, pps in poses.items():
    if decide(pps, L, t):
        ans.append(seq)

print(" ".join(sorted(ans)))
