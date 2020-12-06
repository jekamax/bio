import json
from types import SimpleNamespace
from urllib import parse
import csv
import dump_genbank

#  XPATH от даты /html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[3]
#  ИЛИ document.getElementsByClassName('json_ json_imagemap')[0].textContent

#epigenomes=N/A -- не доказано
#epigenomes=..... --- то что нужно, доказано

origin=166800000 

src=None
with open('data_to_parse_factors_experiment_proven.json', newline='') as file:
    src=json.load(file)

rows=[]
for node in src:
    assert len(node)==3
    params=node[2]
    href=params.get('href')
    if href:
        url=parse.urlparse(href)
        query=parse.parse_qs(url.query)
        epigenomes=query.get('epigenomes',['N/A'])[0]
        if epigenomes!='N/A':

            #  Что значит строка epigenomes? Напр.: HeLa-S3; A549; GM12878; K562; SK-N.; MCF-7; HepG2; H1-hESC_3; HCT116 -- Это клеточные линии
            #  Точно ли эта дата по хомосапиенсу? Имена факторов странные -- Норм, для хомо.

            #  What is right feature id???  -- Хз, похуй
            feature_id=query['feature_id'][0]
            #if feature_id=='ENSM00082363325':
            #    print(query)

            #  MUST VERIFY POSITIONS - Да, маст
            #  Different positions stored in query['r']
            #se=query['r'][0].split(':')[1].split('-')
            #s=int(se[0])
            #e=int(se[1])
            #print((fe-fs),(e-s))
           
            #  MUST VERIFY STRAND -- 
            strand=int(query['fake_click_strand'][0])
            #  Why strand is always -1
            assert strand==-1

            row=SimpleNamespace()
            row.start=int(query['fake_click_start'][0])
            row.end=int(query['fake_click_end'][0])
            row.file_start=row.start-origin
            row.file_end=row.end-origin
            row.factors=query['transcription_factors'][0].replace(',','; ')
            row.id=feature_id
            row.epigenomes=epigenomes.replace(',','; ')
            
            rows.append(row.__dict__)

with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = ['id' , 'start', 'end', 'file_start', 'file_end', 'factors', 'epigenomes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()
    writer.writerows(rows)

with open(f'ensemble.gb', 'w', newline='') as file:
        file.write(dump_genbank.dump_genbank(rows))
