from Bio import SeqIO
from Bio.Alphabet import generic_dna

filename = 'oct1-regions-both-strands'


def renameFeature(feature):
    fq = feature.qualifiers
    name = fq.get('name', 'unknown_name')
    family = fq.get('family', 'unknown_family')
    # fq['comment']=fq.get('comment','no_comment').replace('\n','-')
    fq['ugene_name'] = name
    fq['ugene_group'] = family


def calcAndWriteScore(part):
    score = {}
    for f in part.features:
        for i in f.location:
            score[i] = score.get(i, 0) + 1
    for i in range(1, len(part.seq)):
        score[i] = score.get(i, 0)
    with open(f'{filename}-{part.id}-scores.txt', 'w') as f:
        for i in sorted(score.keys()):
            f.write(f'{i}\t{score[i]}\n')


parts = SeqIO.parse(f'{filename}.gb', 'genbank')
out_parts = []
for part in parts:
    out_parts.append(part)
    print(f'------{part.id}------')
    part.seq.alphabet = generic_dna
    for f in part.features:
        renameFeature(f)
    calcAndWriteScore(part)

SeqIO.write(out_parts, f'{filename}-named.gb', 'genbank')
