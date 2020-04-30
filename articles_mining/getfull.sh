#!/bin/bash

set -euxo pipefail
# curl  \
#    -H "Accept-Encoding: gzip" \
#    "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:7060350&metadataPrefix=pmc" > test.gz

mkdir full_text || true
mkdir full_text/abstract_only || true

while read -r id; do
(
    cd full_text 
    if [ ! -f "$id.xml" ] || [ ! -f "abstract_only/$id.xml" ]; then
        echo "========$id=========="
        curl -L --connect-timeout 5 --retry 3 \
           -H "Accept-Encoding: gzip" \
            "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:$id&metadataPrefix=pmc" \
            | gunzip -c > "$id.xml"
        if grep -q "The metadata format 'pmc' is not supported by the item or by the repository." "$id.xml"; then
        (
            rm -f "$id.xml"
            cd abstract_only
            curl -L --connect-timeout 5 --retry 3 \
           -H "Accept-Encoding: gzip" \
            "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:$id&metadataPrefix=pmc_fm" \
            | gunzip -c > "$id.xml"
        )
        fi
        sleep 1s 
    fi
)
done < ids.csv