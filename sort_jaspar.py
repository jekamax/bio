from Bio import motifs
import pickle
import unidecode
import os, shutil

fh = open("jaspar/homosapiens_810_jaspar.txt")
all_motifs = motifs.parse(fh, "jaspar").to_dict()

metafile = open('metadata.dat', 'rb')
metadata = pickle.load(metafile)
respath = "result"
shutil.rmtree(respath, ignore_errors=True)

for name in all_motifs:
    mt = metadata[name]
    # fix UGENE unicode impotence
    for key in mt:
        if isinstance(mt[key], str):
            mt[key] = unidecode.unidecode(mt[key])
        elif isinstance(mt[key], list):
            l = mt[key]
            for i in range(len(l)):
                if isinstance(l[i], str):
                    l[i] = unidecode.unidecode(l[i])

    termnames = ['family', 'class', 'flat']
    for termname in termnames:
        terms = ['flat'] if termname == 'flat' else mt[termname]
        for term in terms:
            root = f'{respath}/by-{termname}/{term.replace("/", "-").replace(":", "-").strip()}'
            os.makedirs(root, exist_ok=True)
            filename = f'{root}/{name}.pfm'
            out = all_motifs[name].format('pfm').replace('.00', '')
            with open(filename, 'w') as f:
                f.write(out)
            desc = f'{mt["matrix_id"]}	NOT.NUMBER	{mt["name"]}	{", ".join(mt["class"])}	;' \
                   f' acc "{",".join(mt["uniprot_ids"])}" ;' \
                   f' collection "{mt["collection"]}" ;' \
                   f' comment "{mt.get("comment", mt["matrix_id"])}" ;' \
                   f' family "{", ".join(mt["family"])}" ;' \
                   f' medline "{" ".join(mt["pubmed_ids"])}" ;' \
                   f' pazar_tf_id "{",".join(mt["pazar_tf_ids"])}" ;' \
                   f' species "{mt.get("species")[0].get("tax_id")}" ;' \
                   f' tax_group "{mt["tax_group"]}" ;' \
                   f' type "{mt["type"]}" \n'
            print("-----" + desc)
            with open(f'{root}/matrix_list.txt', 'a', encoding="utf-8", newline='\n') as listfile:
                listfile.write(desc)
