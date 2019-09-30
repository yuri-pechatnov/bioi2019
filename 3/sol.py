#!/usr/bin/python

from __future__ import print_function
import sys
from collections import defaultdict

pattern = sys.stdin.readline().strip()
genom = sys.stdin.readline().strip()
d = int(sys.stdin.readline().strip())


def hd(a, b):
    return sum(a[i] != b[i] for i in range(len(a)))


ans = []

for i in range(0, len(genom) - len(pattern) + 1):
    if hd(genom[i:i+len(pattern)], pattern) <= d:
        ans.append(str(i))

print(" ".join(ans))

