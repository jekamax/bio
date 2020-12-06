
import grep_parallel

def check_cancer(text):
    return True

def filter_good(filenames):
    return filenames

grep_parallel.check_cancer=check_cancer
grep_parallel.filter_good=filter_good

if __name__ == '__main__':
    grep_parallel.grep('motif_names.txt','motifs_results.txt', 'motifs_summary.txt')

