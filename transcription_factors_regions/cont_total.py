from Bio import SeqIO
from Bio.Alphabet import generic_dna

filename = 'oct1-regions-both-strands'
class Score:
    count_total = 0
    name = ''
    pass


def calc_scores(part):
    result = {}
    for f in part.features:
        name = f.qualifiers.get('name', 'unknown_name')[0]
        score = result.get(name, Score())
        result[name] = score
        score.name = name
        score.count_total += 1
    result =  result.values()
    result = sorted(result, key=lambda s: s.count_total)
    result.reverse()
    return result


def print_scores(scores, filename):
    with open(filename, 'w') as f:
        f.write('name\tcount_total\n')
        for score in scores:
            f.write(f'{score.name}\t{score.count_total}\n')


parts = SeqIO.parse(f'{filename}.gb', 'genbank')
for part in parts:
    scores = calc_scores(part)
    outfile=f'{filename}-{part.id}-factors-count.txt'
    print(outfile)
    print_scores(scores,outfile)
