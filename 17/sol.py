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

#~ dna, pept = map(str.strip, sys.stdin)

m = int(sys.stdin.readline().strip())


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

# http://education.expasy.org/student_projects/isotopident/htdocs/aa-list.html
pept_masses_text = '''\
A	Ala	C3H5ON	71.03711	71.0788
R	Arg	C6H12ON4	156.10111	156.1875
N	Asn	C4H6O2N2	114.04293	114.1038
D	Asp	C4H5O3N	115.02694	115.0886
C	Cys	C3H5ONS	103.00919	103.1388
E	Glu	C5H7O3N	129.04259	129.1155
Q	Gln	C5H8O2N2	128.05858	128.1307
G	Gly	C2H3ON	57.02146	57.0519
H	His	C6H7ON3	137.05891	137.1411
I	Ile	C6H11ON	113.08406	113.1594
L	Leu	C6H11ON	113.08406	113.1594
K	Lys	C6H12ON2	128.09496	128.1741
M	Met	C5H9ONS	131.04049	131.1926
F	Phe	C9H9ON	147.06841	147.1766
P	Pro	C5H7ON	97.05276	97.1167
S	Ser	C3H5O2N	87.03203	87.0782
T	Thr	C4H7O2N	101.04768	101.1051
W	Trp	C11H10ON2	186.07931	186.2132
Y	Tyr	C9H9O2N	163.06333	163.1760
V	Val	C5H9ON	99.06841	99.1326'''

trans_map = {}

for w in wiki_c.split("\n"):
    p, codons = w.split('\t')
    codons = [c.strip().replace('U', 'T') for c in codons.split(',')]
    for c in codons:
        trans_map[c] = p

pept_mass = {}

for pmtl in pept_masses_text.split("\n"):
    print(pmtl.split('\t'))
    p, name, formula, mass1, mass2 = pmtl.split('\t')
    pept_mass[p] = int(float(mass2))

variants = {0:1}
for cm in range(1, m + 1):
    variants[cm] = sum(variants.get(cm - v, 0) for v in set(pept_mass.values()))

print(variants[m])
