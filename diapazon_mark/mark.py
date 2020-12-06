import csv
from types import SimpleNamespace

origin=166800000


diapA=SimpleNamespace()
diapA.stop=origin+420899
diapA.start=diapA.stop-15000

diapL=SimpleNamespace()
diapL.stop=origin+532512
diapL.start=diapL.stop-15000

def inDiap(start, stop, diap):
    return max(start, diap.start)<=min(stop,diap.stop)

curStart=0
curStop=0



locationsA='''LOCUS       ENHANC_L               15001 bp                         03-DEC-2020
UNIMARK     ENHANC_A annotations
            ENHANC_A
FEATURES             Location/Qualifiers'''
locationsL='''LOCUS       ENHANC_L               15001 bp                         03-DEC-2020
UNIMARK     ENHANC_L annotations
            ENHANC_L
FEATURES             Location/Qualifiers'''

featureTemplate='''
     misc_binding    {ugene_positions}
                     /ugene_name="{factor_name}"
                     /ugene_group="factors_both_gc_ugene"'''

footer='''
//
'''

def read_articles():
    genes = set()
    with open('articles.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            genesStr=row['Gene']
            if genesStr:
                for gene in genesStr.split(','):
                    genes.add(gene.strip().upper())
    print(genes)
    return genes


features={'diapA':locationsA,'diapL':locationsL}

def read_table():
    table = []
    with open('genkards_ugene_kit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            #node=SimpleNamespace()
            #node.row=row
            enhStartStr=row['enh_start']
            enhStopStr=row['enh_end']
            if enhStartStr and enhStopStr:
                curStart=int(enhStartStr)
                curStop=int(enhStopStr)
            if not inDiap(curStart,curStop,diapA) and not inDiap(curStart,curStop,diapL):
                continue
            positionsStr=row['positions'].strip()
            #print(positionsStr)
            newPositions=''
            positionsInFile=''
            diapPositions=''
            diapPositionsFromStop=''
            pos_list=[]
            diapName=None
            if positionsStr:
                poseStrs=positionsStr.split(' ')
                for poseStr in poseStrs:
                    locStr=poseStr.split(':')[0]
                    quant=poseStr.split(':')[1]
                    start=int(locStr.split("-")[0])
                    stop=int(locStr.split("-")[1])
                    diap=None
                    if inDiap(start,stop,diapA):
                        diap=diapA
                        diapName='diapA'
                    if inDiap(start,stop,diapL):
                        diap=diapL
                        diapName='diapL'
                    if diap:
                        row[diapName]='V'
                        newPositions+=f' {start}-{stop}:{quant}'
                        positionsInFile+=f' {start-origin}-{stop-origin}:{quant}'
                        diapPositions+=f' {start-diap.start}-{stop-diap.start}:{quant}'
                        diapPositionsFromStop+=f' {start-diap.stop}-{stop-diap.stop}:{quant}'
                        pos_list.append(f'{start-diap.start}..{min(stop-diap.start,15000)}')
            
            factor_name=row['factor_both']
            if diapName and factor_name:
                ugene_positions=','.join(pos_list)
                if len(pos_list)>1:
                    ugene_positions=f'join({ugene_positions})'
                features[diapName]+=featureTemplate.format_map(locals())



            if row.get('diapA') or row.get('diapL') or enhStartStr or not positionsStr:
                row['positions']=newPositions
                row['positions_in_file']=positionsInFile
                row['positions_from_diap']=diapPositions
                row['positions_from_diap_end']=diapPositionsFromStop
                
                
                table.append(row)
    for feaName in features.keys():
        features[feaName]+=footer
    return table


table=read_table()

for feaName in features.keys():
    with open(f'{feaName}_factors.gb', 'w', newline='') as file:
        file.write(features[feaName])


genes=read_articles()



for row in table:
    if row['factor_genecard'] in genes or row['factor_both'] in genes or row['factor_ugene'] in genes:
        row['in_articles']='V'

with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = ['enhancer', 'enh_start', 'enh_end','in_articles', 'factor_genecard', 'factor_both'
    , 'factor_ugene', 'found_by_kit', 'diapA', 'diapL'
    , 'positions','positions_in_file', 'positions_from_diap', 'positions_from_diap_end']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(table)
