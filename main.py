"""
@author: Thomas Bott
@author: Sebastian Sammet
"""
from tcf_file import TCF_File
from corpus_statistics import Corpus_Statistics
from annotate_relations import Annotation
from docopt import docopt

def main():
    args = docopt("""
    Usage:
        main.py <character_file>
    
    Arguments:
        <character_file> = file containing the character which should be processed, format: one character per line
    """)

    # get arguments
    character_file = args['<character_file>']

    characters = []
    with open(character_file, 'r') as character_file:
        for line in character_file:
            line = line.strip()
            characters.append(line)

    print("Downloading TCF file and setting up the TCF object ...")
    tcf_file = TCF_File()
    print("Computing corpus statistics ...")
    corpus_statistics = Corpus_Statistics(tcf_file)
    corpus_statistics.write_plot_stats()
    print("Adding annotation layers and constructing a new xml document ...")
    annotations = Annotation(tcf_file, characters)
    annotations.construct_new_tree()

if __name__ == "__main__":
    main()