import grep_parallel


if __name__ == '__main__':
    grep_parallel.grep('protein-coding_gene.txt','cancer_gene_results.txt', 'cancer_gene_summary.txt')
