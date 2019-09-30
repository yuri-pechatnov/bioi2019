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

blosum62_h = '''
   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
'''
blosum62 = '''
A  4  0 -2 -1 -2  0 -2 -1 -1 -1 -1 -2 -1 -1 -1  1  0  0 -3 -2
C  0  9 -3 -4 -2 -3 -3 -1 -3 -1 -1 -3 -3 -3 -3 -1 -1 -1 -2 -2
D -2 -3  6  2 -3 -1 -1 -3 -1 -4 -3  1 -1  0 -2  0 -1 -3 -4 -3
E -1 -4  2  5 -3 -2  0 -3  1 -3 -2  0 -1  2  0  0 -1 -2 -3 -2
F -2 -2 -3 -3  6 -3 -1  0 -3  0  0 -3 -4 -3 -3 -2 -2 -1  1  3
G  0 -3 -1 -2 -3  6 -2 -4 -2 -4 -3  0 -2 -2 -2  0 -2 -3 -2 -3
H -2 -3 -1  0 -1 -2  8 -3 -1 -3 -2  1 -2  0  0 -1 -2 -3 -2  2
I -1 -1 -3 -3  0 -4 -3  4 -3  2  1 -3 -3 -3 -3 -2 -1  3 -3 -1
K -1 -3 -1  1 -3 -2 -1 -3  5 -2 -1  0 -1  1  2  0 -1 -2 -3 -2
L -1 -1 -4 -3  0 -4 -3  2 -2  4  2 -3 -3 -2 -2 -2 -1  1 -2 -1
M -1 -1 -3 -2  0 -3 -2  1 -1  2  5 -2 -2  0 -1 -1 -1  1 -1 -1
N -2 -3  1  0 -3  0  1 -3  0 -3 -2  6 -2  0  0  1  0 -3 -4 -2
P -1 -3 -1 -1 -4 -2 -2 -3 -1 -3 -2 -2  7 -1 -2 -1 -1 -2 -4 -3
Q -1 -3  0  2 -3 -2  0 -3  1 -2  0  0 -1  5  1  0 -1 -2 -2 -1
R -1 -3 -2  0 -3 -2  0 -3  2 -2 -1  0 -2  1  5 -1 -1 -3 -3 -2
S  1 -1  0  0 -2  0 -1 -2  0 -2 -1  1 -1  0 -1  4  1 -2 -3 -2
T  0 -1 -1 -1 -2 -2 -2 -1 -1 -1 -1  0 -1 -1 -1  1  5  0 -2 -2
V  0 -1 -3 -2 -1 -3 -3  3 -2  1  1 -3 -2 -2 -3 -2  0  4 -3 -1
W -3 -2 -4 -3  1 -2 -2 -3 -3 -2 -1 -4 -4 -2 -3 -3 -2 -3 11  2
Y -2 -2 -3 -2  3 -3  2 -1 -2 -1 -1 -2 -3 -1 -2 -2 -2 -1  2  7
'''

blosum62_m = [list(map(int, line.split()[1:])) for line in blosum62.strip().split('\n')]
blosum62_chars = blosum62_h.split()

award_m = np.zeros((256, 256), dtype=int)

for i1, c1 in enumerate(blosum62_chars):
    for i2, c2 in enumerate(blosum62_chars):
        award_m[ord(c1), ord(c2)] = blosum62_m[i1][i2]
    award_m[ord(c1), ord('-')] = -5
    award_m[ord('-'), ord(c1)] = -5



def award(c1, c2):
    return award_m[ord(c1), ord(c2)]


#~ print(blosum62_m)
#~ print(blosum62_chars)
#~ print(award('Y', 'Y'))
#~ print(award('M', 'L'))

#~ n, m = map(int, sys.stdin.readline().strip().split())
#~ up = [list(map(int, sys.stdin.readline().strip().split())) for i in range(n)]
#~ assert sys.stdin.readline().strip() == '-'
#~ right = [list(map(int, sys.stdin.readline().strip().split())) for i in range(n + 1)]

a, b = [sys.stdin.readline().strip() for i in range(2)]


print(len(a), len(b))

N = max(len(a), len(b))

d = np.zeros((N + 5, N + 5), dtype=int)
wr = np.zeros((N + 5, N + 5, 2), dtype=int)


for i in range(-1, N):
    d[-1, i] = d[i, -1] = -5 * (i + 1)
    wr[-1, i] = (ord('-'), ord((b + a)[i]))
    wr[i, -1] = (ord((a + b)[i]), ord('-'))


for ai, ac in tqdm(list(enumerate(a))):
    for bi, bc in enumerate(b):
        d[ai, bi], nw = max(
            (d[ai - 1, bi - 1] + award(ac, bc), (ac, bc)),
            (d[ai, bi - 1] + award('-', bc), ('-', bc)),
            (d[ai - 1, bi] + award(ac, '-'), (ac, '-')),
        )
        wr[ai, bi] = (ord(nw[0]), ord(nw[1]))



pos = len(a) - 1, len(b) - 1
print(d[pos])
res = []
while pos != (-1, -1):
    w = wr[pos]
    res.append(w)
    pos = (pos[0] - (w[0] != ord('-')), pos[1] - (w[1] != ord('-')))

for i in range(2):
    print("".join([chr(r[i]) for r in res][::-1]))

#~ PLEASANTLY
#~ -MEA--N-LY

#~ print(sum([award('P', '-'), award('L','M'), award('E','E'),
#~ award('A','A'), award('S','-'), award('A','-'), award('N','N'),
#~ award('T','-'), award('L','L'), award('Y','Y')]))


#~ print(n, m)
#~ print(up)
#~ print(right)

