"""
@author: Thomas Bott
@author: Sebastian Sammet
"""
import csv
import os
from tcf_file import TCF_File
import statistics
import matplotlib.pyplot as plt

class Corpus_Statistics:
    """This class is used to generate corpus statistics and to ouput them.
    """

    def __init__(self, tcf_file:TCF_File, output_dir:str) -> None:
        """Initialize

        Args:
            tcf_file (TCF_File): tcf file object
        """
        self.tcf_file = tcf_file
        self.output_dir = output_dir

        self.tale_stats = []
        for tale_id, sentence_ids in tcf_file.tales_dict.items():
            tale_stats = self.get_tale_stats(tale_id)
            self.tale_stats.append(tale_stats)

        self.full_stats = self.get_full_stats()

    def get_tale_stats(self, tale_id:str) -> dict:
        """This function calculates statistics for a tale.

        Args:
            tale_id (str): tale id

        Returns:
            dict: dictionary containing statistics
        """
        title = " ".join(self.tcf_file.get_sentence(self.tcf_file.tales_dict[tale_id][0])) 
        number_of_sentences = len(self.tcf_file.tales_dict[tale_id]) 
        number_of_tokens = 0 
        lemmas = set()
        mean_sentence_length = []
        tokens_freqs = {}
        lemmas_freqs = {}
        pos_freqs = {}
        nouns_freqs = {}

        for sentence_id in self.tcf_file.tales_dict[tale_id]:
            token_ids = self.tcf_file.sentences_dict[sentence_id]
            sentence_length = len(token_ids)
            mean_sentence_length.append(sentence_length)
            number_of_tokens += len(token_ids)
            for token_id in token_ids:
                lemma = self.tcf_file.lemmas_dict[token_id]
                lemmas.add(lemma)
                token = self.tcf_file.tokens_dict[token_id]
                pos = self.tcf_file.pos_dict[token_id]
                if token in tokens_freqs:
                    tokens_freqs[token] += 1
                else:
                    tokens_freqs[token] = 1
                if lemma in lemmas_freqs:
                    lemmas_freqs[lemma] += 1
                else:
                    lemmas_freqs[lemma] = 1
                if pos in pos_freqs:
                    pos_freqs[pos] += 1
                else:
                    pos_freqs[pos] = 1

                if pos =="NN" or pos == "NE":
                    if lemma in nouns_freqs:
                        nouns_freqs[lemma] += 1
                    else:
                        nouns_freqs[lemma] = 1

        number_of_lemmas = len(lemmas)
        mean_sentence_length = statistics.mean(mean_sentence_length)
        lemma_token_ratio = number_of_lemmas / number_of_tokens
        tokens_freqs = dict(sorted(tokens_freqs.items(), key=lambda item: item[1], reverse=True))
        lemmas_freqs = dict(sorted(lemmas_freqs.items(), key=lambda item: item[1], reverse=True))
        pos_freqs = dict(sorted(pos_freqs.items(), key=lambda item: item[1], reverse=True))
        nouns_freqs = dict(sorted(nouns_freqs.items(), key=lambda item: item[1], reverse=True))
        top10_tokens = dict(list(tokens_freqs.items())[:10])
        top10_lemmas = dict(list(lemmas_freqs.items())[:10])
        top10_pos = dict(list(pos_freqs.items())[:10])
        top10_nouns = dict(list(nouns_freqs.items())[:10])

        stats = {}
        stats["title"] = title
        stats["number_of_sentences"] = number_of_sentences
        stats["number_of_tokens"] = number_of_tokens
        stats["number_of_lemmas"] = number_of_lemmas
        stats["mean_sentence_length"] = mean_sentence_length
        stats["tokens_freqs"] = tokens_freqs
        stats["lemmas_freqs"] = lemmas_freqs
        stats["pos_freqs"] = pos_freqs
        stats["nouns_freqs"] = nouns_freqs
        stats["lemma_token_ratio"] = lemma_token_ratio
        stats["top10_tokens"] = top10_tokens
        stats["top10_lemmas"] = top10_lemmas
        stats["top10_pos"] = top10_pos
        stats["top10_nouns"] = top10_nouns
        return stats

    def get_full_stats(self) -> dict:
        """This function aggregates all tale stats and returns statistics for the full corpus (without Vorwort)

        Returns:
            dict: dictionary conataining statistics
        """
        title = "full corpus"
        number_of_sentences = 0
        number_of_tokens = 0
        number_of_lemmas = 0
        mean_sentence_length = []
        tokens_freqs = {}
        lemmas_freqs = {}
        pos_freqs = {}
        nouns_freqs = {}
        top_nouns_tales = {}
        for tale_stat in self.tale_stats:
            number_of_sentences += tale_stat["number_of_sentences"]
            number_of_tokens += tale_stat["number_of_tokens"]
            number_of_lemmas += tale_stat["number_of_lemmas"]
            mean_sentence_length.append(tale_stat["mean_sentence_length"])
            for token, freq in tale_stat["tokens_freqs"].items():
                if token in tokens_freqs:
                    tokens_freqs[token] += freq
                else:
                    tokens_freqs[token] = freq
            for lemma, freq in tale_stat["lemmas_freqs"].items():
                if lemma in lemmas_freqs:
                    lemmas_freqs[lemma] += freq
                else:
                    lemmas_freqs[lemma] = freq
            for pos, freq in tale_stat["pos_freqs"].items():
                if pos in pos_freqs:
                    pos_freqs[pos] += freq
                else:
                    pos_freqs[pos] = freq
            for noun, freq in tale_stat["nouns_freqs"].items():
                if noun in nouns_freqs:
                    nouns_freqs[noun] += freq
                else:
                    nouns_freqs[noun] = freq
            for noun, freq in tale_stat["top10_nouns"].items():
                if noun in top_nouns_tales:
                    top_nouns_tales[noun] += freq
                else:
                    top_nouns_tales[noun] = freq
        
        mean_sentence_length = statistics.mean(mean_sentence_length)
        lemma_token_ratio = number_of_lemmas / number_of_tokens
        tokens_freqs = dict(sorted(tokens_freqs.items(), key=lambda item: item[1], reverse=True))
        lemmas_freqs = dict(sorted(lemmas_freqs.items(), key=lambda item: item[1], reverse=True))
        pos_freqs = dict(sorted(pos_freqs.items(), key=lambda item: item[1], reverse=True))
        nouns_freqs = dict(sorted(nouns_freqs.items(), key=lambda item: item[1], reverse=True))
        top_nouns_tales = dict(sorted(top_nouns_tales.items(), key=lambda item: item[1], reverse=True))
        top10_tokens = dict(list(tokens_freqs.items())[:10])
        top10_lemmas = dict(list(lemmas_freqs.items())[:10])
        top10_pos = dict(list(pos_freqs.items())[:10])
        top10_nouns = dict(list(nouns_freqs.items())[:10])

        stats = {}
        stats["title"] = title
        stats["number_of_sentences"] = number_of_sentences
        stats["number_of_tokens"] = number_of_tokens
        stats["number_of_lemmas"] = number_of_lemmas
        stats["mean_sentence_length"] = mean_sentence_length
        stats["tokens_freqs"] = tokens_freqs
        stats["lemmas_freqs"] = lemmas_freqs
        stats["pos_freqs"] = pos_freqs
        stats["nouns_freqs"] = nouns_freqs
        stats["lemma_token_ratio"] = lemma_token_ratio
        stats["top10_tokens"] = top10_tokens
        stats["top10_lemmas"] = top10_lemmas
        stats["top10_pos"] = top10_pos
        stats["top10_nouns"] = top10_nouns
        stats["top_nouns_tales"] = top_nouns_tales
        return stats

    def write_plot_stats(self) -> None:
        """This function writes some statistics (tales and full) to csv and generates plots as pngs.
        """
        top_nouns = set()
        number_tale_sentences = []
        corpus_stats_file = os.path.join(self.output_dir, "corpus_stats.tsv")
        with open(corpus_stats_file, "wt") as f:
            tsv_writer = csv.writer(f, delimiter="\t")
            tsv_writer.writerow(["title", "number_of_sentences", "number_of_tokens", "number_of_lemmas", "mean_sentence_length", "lemma_token_ratio", "top_10_nouns"])

            for tale_stat in self.tale_stats:
                number_tale_sentences.append(tale_stat["number_of_sentences"])
                tsv_writer.writerow([tale_stat["title"], tale_stat["number_of_sentences"], tale_stat["number_of_tokens"], tale_stat["number_of_lemmas"], tale_stat["mean_sentence_length"], tale_stat["lemma_token_ratio"], ", ".join(list(tale_stat["top10_nouns"].keys()))])
                for n in list(tale_stat["top10_nouns"].keys()):
                    top_nouns.add(n)

            tsv_writer.writerow([self.full_stats["title"], self.full_stats["number_of_sentences"], self.full_stats["number_of_tokens"], self.full_stats["number_of_lemmas"], self.full_stats["mean_sentence_length"], self.full_stats["lemma_token_ratio"], ", ".join(list(self.full_stats["top10_nouns"].keys()))])

        top50_nouns_file = os.path.join(self.output_dir, "top50_nouns.tsv")
        with open(top50_nouns_file, "wt") as f:
            tsv_writer = csv.writer(f, delimiter="\t")
            tsv_writer.writerow(["top 50 nouns over all tales", "freq"])
            top50 = dict(list(self.full_stats["nouns_freqs"].items())[:50])
            for noun, freq in top50.items():
                tsv_writer.writerow([noun, freq])
                top_nouns.add(noun)
        
        top50_plus_top10Tales_nouns_file = os.path.join(self.output_dir, "top50_plus_top10Tales_nouns.txt")
        with open(top50_plus_top10Tales_nouns_file, "wt") as f:
            for noun in top_nouns:
                f.write(noun + '\n')

        # number of sentences per tail plot
        fig, ax = plt.subplots()
        ax.plot(range(0,len(self.tcf_file.tales_dict)), number_tale_sentences, 'go-')
        ax.set(xlabel='tale id', ylabel='number of sentences', title='number of sentences per tale')
        ax.grid(True)
        figname1 = os.path.join(self.output_dir, "sentences_per_tale.png")
        fig.savefig(figname1)

        #print(number_tale_sentences)
        #print(statistics.mean(number_tale_sentences))
        #print(self.full_stats["pos_freqs"])
        #print(len(self.full_stats["nouns_freqs"]))

        # noun freqs sorted plot
        fig, ax = plt.subplots()
        ax.plot(range(0,len(self.full_stats["nouns_freqs"])), list(self.full_stats["nouns_freqs"].values()), 'yo')
        ax.set(xlabel='noun', ylabel='frequency', title='noun frequency distribution')
        ax.grid(True)
        figname2 = os.path.join(self.output_dir, "noun_frequency_distribution.png")
        fig.savefig(figname2)