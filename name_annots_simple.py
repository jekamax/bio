import re

file = 'all-oct1a'
name_by = 'family'  # or name or class or family
group_by = name_by # or name or class or family


infile = open(f'{file}.gb', newline='\n')
content = infile.read();
infile.close()
splitted = content.split("misc_feature")
renamed = []
for st in splitted:
    namere = re.search(f'/{name_by}="(.*)"', st)
    if namere is not None:
        name = namere.group(1)
        print(name)
        st = re.sub(r'/ugene_name=".*"', f'/ugene_name="{name}"', st)

    familyre = re.search(f'/{group_by}="(.*)"', st)
    if familyre is not None:
        family = familyre.group(1)
        st = re.sub(r'/ugene_group=".*"', f'/ugene_group="{family}"', st)
        print(family)
    renamed.append(st)

with open(f'{file}-by-{name_by}.gb', 'w', newline='\n') as f:
    f.write('misc_feature'.join(renamed))
