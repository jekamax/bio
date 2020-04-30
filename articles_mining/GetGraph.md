#TODO

* Названия: OCT1, OCT 1, OCT-1, POU2F1, OTF. Есть еще написание OCT1/POU2F1. Точно взаимодействует с: SOX9 (или sox2,это  большое семейство), oct2, hoxd9 (или 10), brca1, blacap, per2
* Слова про рак: cancer, carcinoma, tumor, sarcoma, melanoma, lymphoma, myeloma, neuroblastoma, neurofibroma, teratoma, adenoma, meningioma, malignansy, malignant transformation/growth/tumor (короче, malignant что угодно), neoplasm, metastasis, leucemia, leucosis
* Отфильтровать, чтобы в выборку попадали только статьи, где в названии есть слова про канцер
* Сделать фильтр, чтобы смотреть какой ген упомянут в большом разных кол-ве статей

#Steps

##Download human genes

````
ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/tsv/locus_groups/protein-coding_gene.txt
```

## Download all articles about pou2f1 and OCT1

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=pou2f1&retMax=1000
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=OCT1&retMax=1000
```

## MANUAL get only ids

## Remove doublicates

```
sort -n raw_ids.csv | uniq > ids.csv
```

## Get articles

```
./getfull.sh
```


## TODO clear errors

## ?? convert to text ??