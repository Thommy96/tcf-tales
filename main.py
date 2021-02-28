"""
@author: Thomas Bott
@author: Sebastian Sammet
"""
from tcf_file import TCF_File
from tcf_file_vol2 import TCF_File_vol2
from corpus_statistics import Corpus_Statistics
from annotate_relations import Annotation
from docopt import docopt
import pandas as pd

def main():
    args = docopt("""
    Usage:
        main.py <character_file> <category_file> [-v]
    
    Arguments:
        <character_file> = file containing the character which should be processed, format: one character per line
        <category_file> = tsv file containing the categories with the respective nouns, format: one category per column

    Options:
        -v --volume2   include volume 2 of the tales collection (problem: file too large for Neo4j)
    """)

    # get arguments and options
    character_file = args['<character_file>']
    category_file = args['<category_file>']
    is_vol2 = args['--volume2']

    # load characters
    characters = []
    with open(character_file, 'r') as character_file:
        for line in character_file:
            line = line.strip()
            characters.append(line)

    # load categories
    categories = {}
    categories_df = pd.read_csv(category_file, sep='\t', encoding='utf-8')
    categories_df = categories_df.dropna()
    headers = list(categories_df)
    for header in headers:
        categories[header] = set(categories_df[header])
    
    # schneewittchen more detailed analysis
    schneewittchen_characters = ['Königin', 'Gemahlin', 'Frau', 'Stiefmutter', 'Krämerfrau', 'Alte', 'Weib', 'Bauersfrau', 'Bauerin', 'Krämerin', 'Schneewittchen', 'Kind', 'Töchterlein', 'Mädchen', 'Königstochter', 'Spiegel', 'Spieglein', 'Jäger', 'Zwerg', 'Zwerglein', 'Königssohn', 'König', 'Koch']
    for sc in schneewittchen_characters:
        if sc not in characters:
            characters.append(sc)

    # set output directory
    if is_vol2:
        output_dir = '/home/users0/bottts/tcf-tales/vol1_and_vol2/'
    else:
        output_dir = '/home/users0/bottts/tcf-tales/vol1/'

    print("Downloading TCF file and setting up the TCF object ...")
    if is_vol2:
        tcf_file = TCF_File_vol2()
    else:
        tcf_file = TCF_File()
    print("Computing corpus statistics ...")
    corpus_statistics = Corpus_Statistics(tcf_file, output_dir)
    corpus_statistics.write_plot_stats()
    print("Adding annotation layers and constructing a new xml document ...")
    annotations = Annotation(tcf_file, characters, categories, output_dir)
    annotations.construct_new_tree()

if __name__ == "__main__":
    main()