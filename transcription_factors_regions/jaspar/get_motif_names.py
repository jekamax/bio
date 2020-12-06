from Bio import motifs
import pickle
import unidecode
import os, shutil

filename = 'jaspar_homosapiens'

fh = open(f"{filename}.txt")
all_motifs = motifs.parse(fh, "jaspar").to_dict()
fh.close()

names=[]
for motif in all_motifs:
    names.extend(all_motifs[motif].name.split('(')[0].split('::'))

names=list(set(names))
names.sort()
for name in names:
    print(name)
