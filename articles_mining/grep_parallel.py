import csv
import glob
import re
import types
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


def search_flat(job):
    filename = job.filename
    genename = job.genename
    global global_files
    file = global_files.get(filename)
    if not file:
        file = load_file(filename)
        global_files[filename] = file

    result = types.SimpleNamespace()
    result.link = file.link
    result.article_title = file.article_title
    result.found_lines = []

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
    gene = types.SimpleNamespace()
    gene = types.SimpleNamespace()
    gene.name = name
    nameholder = fr'[^a-z]{name.lower()}[^a-z]'
    gene.pattern = re.compile(nameholder)
    return gene


def load_file(filename):
    file = types.SimpleNamespace()
    file.name = filename
    doc = ET.parse(filename)
    xml_doc = doc.getroot()
    content = ''

    article_id = xml_doc.findtext(".//*[@pub-id-type='pmcid']")
    assert(article_id)
    file.link = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/'

    elements = xml_doc.findall('.//*')

    for element in elements:
        if element.tag.endswith('article-meta'):
            for sub in element.findall('.//*'):
                if sub.tag.endswith('article-title'):
                    article_title = "".join(sub.itertext())
                    article_title = article_title.replace(
                        '\t', ' ').replace('\n', ' ').strip()
                    assert article_title, f'file: {filename}'
                    file.article_title = article_title
                    break
            break

    for element in elements:
        if(element.tag.endswith('table')):
            element.clear()
        if(element.tag.endswith('tbody')):
            element.clear()

    elements = xml_doc.findall('.//*')
    for element in elements:
        if element.tag.endswith('abstract') or element.tag.endswith('body'):
            content += ET.tostring(element, encoding='utf-8',
                                   method='text').decode("utf-8")
    assert(len(content) > 0)

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


def read_gene_names():
    names = []
    with open('protein-coding_gene.txt', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            name = row['symbol']
            names.append(name)
    return names


if __name__ == '__main__':
    f = open("results.csv", "w", encoding='utf-8', buffering=1)

    def pr(st):
        print(st)
        f.write(st+'\n')

    names = read_gene_names()
    print(f'Names: {len(names)}')
    files = list(glob.iglob('full_text/**/*.xml', recursive=True))

    try:
        pool = Pool(initializer=init_worker)
        pr('Gene name\tArticle number\tPhrase\tArticle Title\tLink')
        for name in names:
            jobs = []
            for file in files:
                job = types.SimpleNamespace()
                job.filename = file
                job.genename = name
                jobs.append(job)
            # worker_results=[]
            # for job in jobs:
            #    worker_results.append(search_flat(job))
            worker_results = pool.map(search_flat, jobs)
            article_counter = 1
            for worker_result in worker_results:
                if len(worker_result.found_lines) > 0:
                    for line in worker_result.found_lines:
                        pr(f'{name}\t{article_counter}\t{line}\t{worker_result.article_title}\t{worker_result.link}')
                    article_counter += 1
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()

    f.close()
