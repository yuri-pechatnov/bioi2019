#!/usr/bin/python

from __future__ import print_function
import sys
from collections import defaultdict

valmap = defaultdict(int, {
    'C': -1,
    'G': +1,
})

genom = sys.stdin.readline().strip()
vals = [valmap[c] for c in genom]

cumvals = [0]
for v in vals:
    cumvals.append(cumvals[-1] + v)

mcv = min(cumvals)

ans = []

for i, cv in enumerate(cumvals):
    if cv == mcv:
        ans.append(str(i))

print(" ".join(ans))

