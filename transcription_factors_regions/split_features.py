import re, os, unidecode

file = 'test'
name_by_term = 'name'  # or name or class or family
group_by_term = 'family' # or name or class or family

name_by_single_file = 'family'  # or name or class or family
group_by_single_file = 'family' # or name or class or family


infile = open(f'{file}.gb',encoding="utf-8", newline='\n')
filestr = infile.read()
infile.close()


########## split ############
content=filestr
footer='//\n'
assert content[-len(footer):]==footer
content=content[:-len(footer)]

splitter='     misc_feature'
splitted = content.split(splitter)

header=splitted[0]
splitted=splitted[1:]


groups={}

for st in splitted:
    name_by_re = re.search(f'/{name_by_term}="(.*)"', st)
    assert name_by_re is not None
    name = name_by_re.group(1)
    print(name)
    st = re.sub(r'/ugene_name=".*"', f'/ugene_name="{name}"', st)

    group_by_re = re.search(f'/{group_by_term}="(.*)"', st)
    group_name= group_by_re.group(1) if group_by_re else f'unknown_{group_by_term}'
    group_name= group_name or f'unknown_{group_by_term}'
    #st = re.sub(r'/ugene_group=".*"', f'/ugene_group="{group_name}"', st)
    print(group_name)
    group= groups.get(group_name) or []
    group.append(st)
    groups[group_name]=group

root=f'{file}-by-{group_by_term}'
os.makedirs(root, exist_ok=True)
for group in groups:
    print(group)
    result=header+splitter+splitter.join(groups[group])+footer
    fixed_group_name=unidecode.unidecode(group).replace("/","-").replace(":","-").strip()
    with open(f'{root}/annotations-{file}-{fixed_group_name}.gb', 'w',encoding="utf-8", newline='\n') as f:
        f.write(result)

########### groupped ################
content=filestr
splitted = content.split("misc_feature")
renamed = []
for st in splitted:
    namere = re.search(f'/{name_by_single_file}="(.*)"', st)
    if namere is not None:
        name = namere.group(1)
        print(name)
        st = re.sub(r'/ugene_name=".*"', f'/ugene_name="{name}"', st)

    familyre = re.search(f'/{group_by_single_file}="(.*)"', st)
    if familyre is not None:
        family = familyre.group(1)
        st = re.sub(r'/ugene_group=".*"', f'/ugene_group="{family}"', st)
        print(family)
    renamed.append(st)

with open(f'{file}-by-{name_by_single_file}.gb', 'w', newline='\n') as f:
    f.write('misc_feature'.join(renamed))
