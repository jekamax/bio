from Bio import SeqIO
from Bio.Alphabet import generic_dna

strlen = 100
pad_size = 3


def overlap(s, location):
    return max(s.start, location.start) < min(s.stop, location.end)


def assure_place(lines, line):
    fstart = len(line) - len(line.lstrip())
    fend = len(line.rstrip())
    for i in range(len(lines)):
        if len(lines[i][fstart:fend].strip()) == 0:
            return i
    return -1


def put_in_place(lines, line):
    pos = assure_place(lines, line)
    if pos >= 0:
        b_a = bytearray(lines[pos], 'utf-8')
        b_b = bytearray(line, 'utf-8')
        result = bytearray(' ' * 1000, 'utf-8')
        for i in range(len(b_a)):
            result[i] = b_a[i]
        for i in range(len(b_b)):
            if result[i] == 32:  # FIXME magic char
                result[i] = b_b[i]
        size=max(len(result.decode('utf-8').rstrip()),strlen+pad_size)
        rr=result.decode('utf-8')[:size]
        lines[pos] = result.decode('utf-8')[:size]
    else:
        lines.append(str.ljust(line,strlen+pad_size))


def label_feature(f):
    score = round(float(f.qualifiers["Score"][0]))
    return f' {str(f.qualifiers["name"][0])} ({score})'#{f.location.start}'

def hatchline(s,pad,size):
    r=s[:pad]
    grey=True
    for i in range(pad,len(s),size):
        r+=f'<span style="background-color: #F0F0F0;">{s[i:i+size]}</span>' if grey else s[i:i+size]
        grey=not grey
    return r

def ruleline(pad,start,stop,size):
    r=' '*pad
    for i in range(start,stop,size):
        r+=str.rjust(f'{i+size}',size,' ')
    return r


def prnpart(part):
    result=''
    fullpad=6


    pad = ' ' * pad_size
    dots = '.' * pad_size
    for i in range(0, len(part.seq), strlen):
        part_result=''
        reg = slice(i, min(i + strlen, len(part.seq)))
        feature_lines = []
        part.features.sort(key=lambda f: f.strand)
        for f in part.features:
            if overlap(reg, f.location):
                feature_padding_length = max(f.location.start - reg.start, 0)
                feture_body_length = min(f.location.end - reg.start, strlen) - feature_padding_length
                assert feture_body_length > 0
                start_sign = '<' if f.location.start >= reg.start else '-'
                end_sign = '>' if f.location.end <= reg.stop else '-'
                start_tag = pad if f.location.start >= reg.start else dots
                end_tag = '' if f.location.end <= reg.stop else dots
                feature_line = start_tag
                feature_line += ' ' * feature_padding_length
                if f.strand == 1:
                    feature_line += '-' * (feture_body_length - 1)  # place for start_sign,end_sign
                    feature_line += end_sign
                else:
                    feature_line += start_sign
                    feature_line += '-' * (feture_body_length - 1)  # place for start_sign,end_sign
                feature_line += end_tag
                feature_line += label_feature(f)
                put_in_place(feature_lines, feature_line)
        feature_lines.reverse()
        i = 1
        for line in feature_lines:
            l=f'{str.rjust(str(i), 3)}{line}\n'
            part_result+=hatchline(l,fullpad,10)
            i += 1
        seqline=f'{str.rjust(str(reg.start+1), 5)} {part.seq[reg]} {reg.stop}\n'
        part_result+=hatchline(seqline,fullpad,10)
        part_result+=hatchline(ruleline(fullpad,reg.start,reg.stop,10),fullpad,10)+'\n'
        result+=f'<p><pre>{part_result}</pre></p>'
    return result


filename = 'oct1-regions-both-strands-named'
parts = SeqIO.parse(f'{filename}.gb', 'genbank')
content='<html><body>\n'
for part in parts:
    text=prnpart(part)
    content+=f'<h3>{part.name}</h3>{text}<hr>'
content+='</html></body>\n'
with open(f'{filename}-match-format.html', 'w', newline='\n') as f:
    f.write(content)
