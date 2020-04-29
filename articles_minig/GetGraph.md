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