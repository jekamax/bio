import csv, glob, re, types, sys, signal
from multiprocessing import Pool
import xml.etree.ElementTree as ET


def load_file(filename):
    file=types.SimpleNamespace()
    file.name=filename
    doc=ET.parse(filename)
    xml_doc=doc.getroot()
    content=''
    
    article_id=xml_doc.findtext(".//*[@pub-id-type='pmcid']")
    assert(article_id)
    file.link=f'https://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/'
    print(file.link)

    
    elements=xml_doc.findall('.//*')
    for element in elements:
        if(element.tag.endswith('article-meta')):
            for sub in element.findall('.//*'):
                if sub.tag.endswith('article-title'):
                    article_title=sub.text.replace('\t',' ').replace('\n',' ').strip()
                    assert(article_title)
                    file.article_title=article_title
        if(element.tag.endswith('table')):
            element.clear()
        if(element.tag.endswith('tbody')):
            element.clear()
        

    elements=xml_doc.findall('.//*')
    for element in elements:
        if element.tag.endswith('abstract') or element.tag.endswith('body'):
            content+=ET.tostring(element,encoding='utf-8',method='text').decode("utf-8")
    
    lines=content.split('\n')
    result=[]
    for line in lines:
        stripped=line.strip()
        if stripped:
            for sentence in stripped.split('.'):
                s=sentence.strip()
                if s:
                    result.append(s)            

    assert(len(content)>0)
    file.content = result
    return file


if __name__ == '__main__':
    f = open("gettext.txt", "w", encoding='utf-8',buffering=1)
    for line in load_file('full_text/4370735.xml').content:
        f.write(line+'\n')
    f.close()