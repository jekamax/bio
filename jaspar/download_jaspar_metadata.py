from Bio import motifs
import coreapi
import pickle

filename = 'jaspar_homosapiens'

fh = open(f"{filename}.txt")
all_motifs = motifs.parse(fh, "jaspar").to_dict()

client = coreapi.Client()
schema = client.get("http://jaspar.genereg.net/api/v1/docs")
action = ["matrix", "read"]


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

data = {}
for name in all_motifs:
    filename = name + '.' + all_motifs[name].name.replace(':', '-') + '.pfm'
    out = all_motifs[name].format('pfm').replace('.00', '')
    params = {
        "matrix_id": name,
    }
    result = client.action(schema, action, params=params)
    print("-----" + str(result))
    data[name] = result;
save_object(data, f'{filename}_metadata.dat')
