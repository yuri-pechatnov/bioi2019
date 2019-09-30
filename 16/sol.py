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
import sys

sys.setrecursionlimit(100000)

# previous solutions was very slow :(
# try to fasten with numpy

mers = "ATCG"
mers_a = np.fromstring(mers, np.int8)
c2n = np.zeros(255, dtype=np.int8)
c2n[mers_a] = np.arange(len(mers))

def S(a):
    return mers_a[a].tostring()

def A(s):
    return c2n[np.fromstring(s, np.int8)]


assert S(A("ATCGAAATTTCCCGGG")) == "ATCGAAATTTCCCGGG"


def hd(a, b):
    return (a != b).sum()

#~ k, d = map(int, sys.stdin.readline().strip().split())
#~ kmers = list(map(str.strip, sys.stdin))
#~ kmersA = [[A(s.split('|')[i]) for s in kmers] for i in range(2)]
#~ n = len(kmers)

dna, pept = map(str.strip, sys.stdin)


def rev_compl(g):
    return S(A(g) ^ 1)[::-1]

#~ print(rev_compl("ACGTAACCGGTT"))

# https://en.wikipedia.org/wiki/Genetic_code#RNA_codon_table
wiki_c = '''\
A	GCU, GCC, GCA, GCG
R	CGU, CGC, CGA, CGG, AGA, AGG
N	AAU, AAC
D	GAU, GAC
C	UGU, UGC
Q	CAA, CAG
E	GAA, GAG
G	GGU, GGC, GGA, GGG
H	CAU, CAC
I	AUU, AUC, AUA
L	UUA, UUG, CUU, CUC, CUA, CUG
K	AAA, AAG
M	AUG
F	UUU, UUC
P	CCU, CCC, CCA, CCG
S	UCU, UCC, UCA, UCG, AGU, AGC
T	ACU, ACC, ACA, ACG
W	UGG
Y	UAU, UAC
V	GUU, GUC, GUA, GUG'''

trans_map = {}

for w in wiki_c.split("\n"):
    p, codons = w.split('\t')
    codons = [c.strip().replace('U', 'T') for c in codons.split(',')]
    for c in codons:
        trans_map[c] = p

print(trans_map)


def translate(g):
    assert len(g) % 3 == 0
    res = []
    for i in range(0, len(g), 3):
        res.append(trans_map.get(g[i:i+3], '?'))
    return "".join(res)

def check1(g, p):
    return translate(g) == p


def check(g, p):
    return check1(g, p) or check1(rev_compl(g), p)

for i in range(len(dna) - 3 * len(pept) + 1):
    cand = dna[i:i+3*len(pept)]
    if check(cand, pept):
        print(cand)

