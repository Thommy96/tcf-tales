from tcf_file import TCF_File
from corpus_statistics import Corpus_Statistics
from annotate_relations import Annotation
from docopt import docopt

def main():
    args = docopt("""
    Usage:
        corpus_statistics.py <corpus_path> <character_file>
    
    Arguments:
        <corpus_path> = path to corpus in tcf format
        <character_file> = file containing the character which should be processed, format: one character per line
    """)

    # get arguments
    corpus_path = args['<corpus_path>']
    character_file = args['<character_file>']

    characters = []
    with open(character_file, 'r') as character_file:
        for line in character_file:
            line = line.strip()
            characters.append(line)

    tcf_file = TCF_File(corpus_path)
    corpus_statistics = Corpus_Statistics(tcf_file)
    corpus_statistics.write_plot_stats()
    annotations = Annotation(tcf_file, characters)
    annotations.construct_new_tree()

if __name__ == "__main__":
    main()