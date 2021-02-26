import pandas as pd
import itertools
import csv

if __name__ == "__main__":

    stats_df = pd.read_csv('corpus_stats.tsv', sep='\t', encoding='utf-8')
    top_list = stats_df['top_10_nouns'].tolist()
    tale_similarity = {}
    for a, b in itertools.combinations(top_list, 2):
        a_list = a.split(',')
        b_list = b.split(',')
        similarity = len(set(a_list) & set(b_list))
        sim_nouns = set(a_list) & set(b_list)
        sim_nouns = ', '.join(str(n) for n in sim_nouns)
        index_a = top_list.index(a)
        index_b = top_list.index(b)
        title_a = stats_df['title'][index_a]
        title_b = stats_df['title'][index_b]
        tale_similarity[(title_a, title_b, sim_nouns)] = similarity
    
    tale_similarity = dict(sorted(tale_similarity.items(), key=lambda item: item[1], reverse=True))
    
    with open('similar_tales.tsv', 'wt') as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(['tales', 'similarity (overlap of top 10 nouns)', 'nouns'])
        for tales, sim in tale_similarity.items():
            tsv_writer.writerow([tales[0] + ', ' + tales[1], sim, tales[2]])