import csv
import glob
import re
import types
from types import SimpleNamespace
import sys
import signal
from multiprocessing import Pool
import xml.etree.ElementTree as ET
import pickle
import os.path

global_genes = {}
global_files = {}


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def filter_good(filenames):
    goods=[]
    for filename in filenames:
        file=load_file(filename)
        if not file.bad:
            goods.append(filename)
    return goods



def search_flat(job):
    filename = job.filename
    genename = job.genename
    global global_files
    file = global_files.get(filename)
    if not file:
        file = load_file(filename)
        global_files[filename] = file

    result = SimpleNamespace()
    result.link = file.link
    result.article_title = file.article_title
    result.found_lines = []

    if file.bad:
        return result

    global global_genes
    gene = global_genes.get(genename)
    if not gene:
        gene = make_pattern(genename)
        if not gene:
            return result
        global_genes[genename] = gene

    for line in file.content:
        testline = line.lower()
        if testline.find('oct1') > 0 or testline.find('pou2f1') > 0:
            foundgene = gene.pattern.search(testline)
            if foundgene:
                result.found_lines.append(line)
    return result


def make_pattern(name):
    if name.lower() == 'oct1' or name.lower() == 'pou2f1':
        return None
    gene = SimpleNamespace()
    gene.name = name
    nameholder = fr'[^a-z]{name.lower()}[^a-z]'
    gene.pattern = re.compile(nameholder)
    return gene

def check_cancer(text):
    words=['cancer', 'carcinoma', 'tumor', 'sarcoma', 'melanoma',
     'lymphoma', 'myeloma', 'neuroblastoma', 'neurofibroma', 'teratoma', 
     'adenoma', 'meningioma', 'malignansy', 'malignant', 'neoplasm', 
     'metastasis', 'leucemia', 'leucosis', 'invasive']
    for word in words:
        if text.find(word)>0: return True
    return False

def load_file(filename):
    file = SimpleNamespace()
    file.name = filename
    file.bad=False
    doc = ET.parse(filename)
    xml_doc = doc.getroot()
    content = ''

    # clear namespaces of tags
    for element in xml_doc.iter():
        element.tag=element.tag.split("}")[1]

    title_elem=xml_doc.find(".//article-meta//article-title")
    title="".join(title_elem.itertext())
    assert title, f'file: {filename}'
    file.article_title = title.replace('\t', ' ').replace('\n', ' ').strip()

    article_id = xml_doc.findtext(".//*[@pub-id-type='pmcid']")
    assert(article_id)
    file.link = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/'

    elements = xml_doc.findall('.//*')
    for element in elements:
        if element.tag.endswith('table'):
            element.clear()
        if element.tag.endswith('tbody'):
            element.clear()

    abstract_elements = xml_doc.find('.//abstract')
    abstract="".join(abstract_elements.itertext())
    assert abstract, f'file: {filename}'

    if not check_cancer(title) and not check_cancer(abstract) :
            file.bad=True
            return file

    content=abstract
    body_element=xml_doc.find('.//body')
    if body_element:
        content += ET.tostring(body_element, encoding='utf-8',method='text').decode("utf-8")
    
    lines = content.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            for sentence in stripped.split('.'):
                s = sentence.strip().replace('\t', ' ')
                if s:
                    result.append(s)

    file.content = result
    return file


def read_gene_names(filename):
    names = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            name = row['symbol']
            names.append(name)
    return names


def grep(namesfilename,result_filename, summary_filename):
    files = list(glob.iglob('full_text/**/*.xml', recursive=True))
    
    goods=filter_good(files)
    print(f"Good files: {len(goods)} of {len(files)}")
    files=goods

    f = open(result_filename, 'w', encoding='utf-8', buffering=1)

    def pr(st):
        print(st)
        f.write(st+'\n')

    names = read_gene_names(namesfilename)
    print(f'Names: {len(names)}')

    try:
        summary=[]
        pool = Pool(initializer=init_worker)
        pr('Gene name\tArticle number\tPhrase\tArticle Title\tLink')
        for name in names:
            jobs = []
            for file in files:
                job = SimpleNamespace()
                job.filename = file
                job.genename = name
                jobs.append(job)
            # worker_results=[]
            # for job in jobs:
            #    worker_results.append(search_flat(job))

            worker_results = pool.map(search_flat, jobs)
            
            worker_results=list(filter(lambda res: len(res.found_lines)>0,worker_results))
            
            if len(worker_results)>0:
                geneitem=SimpleNamespace()
                geneitem.name=name
                geneitem.worker_results=worker_results
                summary.append(geneitem)

            for article_counter,worker_result in enumerate(worker_results):
                for line in worker_result.found_lines:
                    pr(f'{name}\t{article_counter+1}\t{line}\t{worker_result.article_title}\t{worker_result.link}')
        pool.close()
        pool.join()

        summary.sort(key=lambda item: len(item.worker_results), reverse=True)
        with open(summary_filename,'w', encoding='utf-8') as sumfile:
            sumfile.write('Gene No\tGene\tTotal Articles\tArticle No\tTitle\tLink\tContent\n')
            for gene_no, geneitem in enumerate(summary):
                gene_name=geneitem.name
                total_articles=len(geneitem.worker_results)
                print(f'{gene_name}: {total_articles}')
                for article_no, worker_result in enumerate(geneitem.worker_results):
                    content=". ".join(worker_result.found_lines)
                    sumfile.write(f'{gene_no+1}\t{gene_name}\t{total_articles}\t{article_no+1}')
                    sumfile.write(f'\t{worker_result.article_title}\t{worker_result.link}\t{content}\n')
                    
        


    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()

    f.close()
