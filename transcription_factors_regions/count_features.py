file = 'oct1a-enhancer'

infile = open(f'{file}.gb', encoding="utf-8", newline='\n')
content = infile.read()
infile.close()

footer = '//\n'
assert content[-len(footer):] == footer
content = content[:-len(footer)]

splitter = '     misc_feature'
splitted = content.split(splitter)

header = splitted[0]
splitted = splitted[1:]
print(f'Features found: {len(splitted)}')
