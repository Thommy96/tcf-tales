import xml.etree.ElementTree as ET
import statistics
import csv
from xml.dom import minidom
import itertools

class TCF_File:

    def __init__(self):
        self.tree = ET.parse("grimm_maerchen_taleslayer.tcf.xml")
        self.tokens = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}tokens")[0]
        self.tokens_dict = {}
        for token in self.tokens:
            token_id = token.attrib["ID"]
            token_value = token.text
            self.tokens_dict[token_id] = token_value

        self.lemmas = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}lemmas")[0]
        self.lemmas_dict = {}
        for lemma in self.lemmas:
            token_id = lemma.attrib["tokenIDs"]
            lemma_value = lemma.text
            self.lemmas_dict[token_id] = lemma_value

        self.POStags = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}POStags")[0]
        self.pos_dict = {}
        for pos in self.POStags:
            token_id = pos.attrib["tokenIDs"]
            pos_value = pos.text
            self.pos_dict[token_id] = pos_value

        self.sentences = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}sentences")[0]
        self.sentences_dict = {}
        for sentence in self.sentences:
            sentence_id = sentence.attrib["ID"]
            token_ids = sentence.attrib["tokenIDs"].split()
            self.sentences_dict[sentence_id] = token_ids

        self.orthography = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}orthography")[0]
        self.corrections_dict = {}
        for correction in self.orthography:
            token_id = correction.attrib["tokenIDs"]
            correction_value = correction.text
            self.corrections_dict[token_id] = correction_value
        
        self.tales = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}tales")[0]
        self.tales_dict = {}
        for tale in self.tales:
            tales_id = tale.attrib["ID"]
            sentence_ids = tale.attrib["sentenceIDs"].split()
            self.tales_dict[tales_id] = sentence_ids

    def get_sentence(self, sentence_id):
        token_ids = self.sentences_dict[sentence_id]
        sentence = []
        for token_id in token_ids:
            token = self.tokens_dict[token_id]
            sentence.append(token)
        return sentence

    def get_freqs(self, d:dict):
        freq_dict = {}
        for token_id, text in d.items():
            if text in freq_dict:
                freq_dict[text] += 1
            else:
                freq_dict[text] = 1
        return freq_dict

    def get_tale_stats(self, tale_id:str):
        """
        title
        number_of_sentences
        number_of_tokens
        number_of_lemmas
        mean_sentence_length
        tokens_freqs
        lemmas_freqs
        pos_freqs
        nouns_freqs
        lemma_token_ratio
        top10_tokens
        top10_lemmas
        top10_pos
        top10_nouns
        """
        title = " ".join(self.get_sentence(self.tales_dict[tale_id][0])) 
        number_of_sentences = len(self.tales_dict[tale_id]) 
        number_of_tokens = 0 
        lemmas = set()
        mean_sentence_length = []
        tokens_freqs = {}
        lemmas_freqs = {}
        pos_freqs = {}
        nouns_freqs = {}

        for sentence_id in self.tales_dict[tale_id]:
            token_ids = self.sentences_dict[sentence_id]
            sentence_length = len(token_ids)
            mean_sentence_length.append(sentence_length)
            number_of_tokens += len(token_ids)
            for token_id in token_ids:
                lemma = self.lemmas_dict[token_id]
                lemmas.add(lemma)
                token = self.tokens_dict[token_id]
                pos = self.pos_dict[token_id]
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

    def get_full_stats(self, stats_list:list):
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
        for s in stats_list:
            number_of_sentences += s["number_of_sentences"]
            number_of_tokens += s["number_of_tokens"]
            number_of_lemmas += s["number_of_lemmas"]
            mean_sentence_length.append(s["mean_sentence_length"])
            for token, freq in s["tokens_freqs"].items():
                if token in tokens_freqs:
                    tokens_freqs[token] += freq
                else:
                    tokens_freqs[token] = freq
            for lemma, freq in s["lemmas_freqs"].items():
                if lemma in lemmas_freqs:
                    lemmas_freqs[lemma] += freq
                else:
                    lemmas_freqs[lemma] = freq
            for pos, freq in s["pos_freqs"].items():
                if pos in pos_freqs:
                    pos_freqs[pos] += freq
                else:
                    pos_freqs[pos] = freq
            for noun, freq in s["nouns_freqs"].items():
                if noun in nouns_freqs:
                    nouns_freqs[noun] += freq
                else:
                    nouns_freqs[noun] = freq
            for noun, freq in s["top10_nouns"].items():
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

def write_stats(tcf_file:TCF_File):
    tcf_file = TCF_File()
    stats_list = []
    with open("corpus_stats.tsv", "wt") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(["title", "number_of_sentences", "number_of_tokens", "number_of_lemmas", "mean_sentence_length", "lemma_token_ratio"])
        for tale_id, sentence_ids in tcf_file.tales_dict.items():
            tale_stats = tcf_file.get_tale_stats(tale_id)
            stats_list.append(tale_stats)
            tsv_writer.writerow([tale_stats["title"], tale_stats["number_of_sentences"], tale_stats["number_of_tokens"], tale_stats["number_of_lemmas"], tale_stats["mean_sentence_length"], tale_stats["lemma_token_ratio"]])
        full_stats = tcf_file.get_full_stats(stats_list)
        tsv_writer.writerow([full_stats["title"], full_stats["number_of_sentences"], full_stats["number_of_tokens"], full_stats["number_of_lemmas"], full_stats["mean_sentence_length"], full_stats["lemma_token_ratio"]])
    
    top_nouns_full = {}
    top_nouns_tales = {}
    for noun, freq in full_stats["nouns_freqs"].items():
        if freq >= 20:
            top_nouns_full[noun] = freq
    for noun, freq in full_stats["top_nouns_tales"].items():
        if freq >= 20:
            top_nouns_tales[noun] = freq

    with open("top_nouns_20.tsv", "wt") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(["top_nouns_full", "freq_full", "top_nouns_tales", "freq_tales"])
        for (full_noun, full_freq), (tales_noun, tales_freq) in zip(top_nouns_full.items(), top_nouns_tales.items()):
            tsv_writer.writerow([full_noun, full_freq, tales_noun, tales_freq])

def explore_relations(tcf_file:TCF_File, characters:list):
    character_combinations = list(itertools.combinations(characters, 2))
    character_freqs_total = {}
    character_freqs_tales = {}
    relation_freqs_total = {}
    relation_freqs_tales = {}

    for tale_id, sentence_ids in tcf_file.tales_dict.items():
        for sentence_id in sentence_ids:
            sentence_lemmas = []
            for token_id in tcf_file.sentences_dict[sentence_id]:
                lemma = tcf_file.lemmas_dict[token_id]
                sentence_lemmas.append(lemma)
                if lemma in characters:
                    if lemma in character_freqs_total:
                        character_freqs_total[lemma] += 1
                    else:
                        character_freqs_total[lemma] = 1
                    if lemma in character_freqs_tales:
                        if tale_id in character_freqs_tales[lemma]:
                            character_freqs_tales[lemma][tale_id] += 1
                        else:
                            character_freqs_tales[lemma][tale_id] = 1
                    else:
                        character_freqs_tales[lemma] = {}
                        character_freqs_tales[lemma][tale_id] = 1
            for character_combination in character_combinations:
                if character_combination[0] in sentence_lemmas and character_combination[1] in sentence_lemmas:
                    if character_combination in relation_freqs_total:
                        relation_freqs_total[character_combination] += 1
                    else:
                        relation_freqs_total[character_combination] = 1
                    if character_combination in relation_freqs_tales:
                        if tale_id in relation_freqs_tales[character_combination]:
                            relation_freqs_tales[character_combination][tale_id] += 1
                        else:
                            relation_freqs_tales[character_combination][tale_id] = 1
                    else:
                        relation_freqs_tales[character_combination] = {}
                        relation_freqs_tales[character_combination][tale_id] = 1
    
    return character_freqs_total, character_freqs_tales, relation_freqs_total, relation_freqs_tales

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def construct_new_tree(tcf_file:TCF_File, explore_list):
    root_node = ET.Element('TextCorpus')

    comment = ET.Comment('tales without metadata, orthography and Vorwort, for easier processing with neo4j')
    root_node.append(comment)

    tales_node = ET.SubElement(root_node, 'tales')
    sentences_node = ET.SubElement(root_node, 'sentences')
    tokens_node = ET.SubElement(root_node, 'tokens')
    lemmas_node = ET.SubElement(root_node, 'lemmas')
    tags_node = ET.SubElement(root_node, 'POStags')
    characters_node = ET.SubElement(root_node, 'characters')
    relations_node = ET.SubElement(root_node, 'relations')

    tale_elements = []
    sentence_elements = []
    token_elements = []
    lemma_elements = []
    tag_elements = []
    character_elements = []
    relation_elements = []

    for tale_id, sentence_ids in tcf_file.tales_dict.items():
        #tale
        tale_title = " ".join(tcf_file.get_sentence(sentence_ids[0]))
        sentence_ids_string = " ".join(sentence_ids)
        tale_element = ET.Element('tale', {'ID':tale_id, 'title':tale_title, 'sentenceIDs':sentence_ids_string})
        tale_elements.append(tale_element)

        #sentence
        for sentence_id in sentence_ids:
            token_ids = tcf_file.sentences_dict[sentence_id]
            token_ids_string = " ".join(token_ids)
            sentence_element = ET.Element('sentence', {'ID':sentence_id, 'tokenIDs':token_ids_string})
            sentence_elements.append(sentence_element)
        
            #token
            for token_id in token_ids:
                token_element = ET.Element('token', {'ID':token_id})
                token_element.text = tcf_file.tokens_dict[token_id]
                token_elements.append(token_element)

                #lemma
                lemma_element = ET.Element('lemma', {'tokenIDs':token_id})
                lemma_element.text = tcf_file.lemmas_dict[token_id]
                lemma_elements.append(lemma_element)

                #tag
                tag_element = ET.Element('tag', {'tokenIDs':token_id})
                tag_element.text = tcf_file.pos_dict[token_id]
                tag_elements.append(tag_element)
    
    character_id_dict = {}
    id_counter = 0
    for character, freq in explore_list[0].items():
        character_id = 'c' + str(id_counter)
        character_id_dict[character] = character_id
        id_counter += 1
        tale_ids = " ".join(list(explore_list[1][character].keys()))
        str_freqs = [str(freq) for freq in list(explore_list[1][character].values())]
        tale_freqs = " ".join(str_freqs)
        character_element = ET.Element('character', {'ID':character_id, 'freq':str(freq), 'taleIDs':tale_ids, 'taleFreqs':tale_freqs})
        character_element.text = character
        character_elements.append(character_element)

    id_counter = 0
    for character_combination, freq in explore_list[2].items():
        relation_id = 'r' + str(id_counter)
        id_counter += 1
        character_ids = " ".join([character_id_dict[character_combination[0]], character_id_dict[character_combination[1]]])
        tale_ids = " ".join(list(explore_list[3][character_combination].keys()))
        str_freqs = [str(freq) for freq in list(explore_list[3][character_combination].values())]
        tale_freqs = " ".join(str_freqs)
        relation_element = ET.Element('relation', {'ID':relation_id, 'freq':str(freq), 'characterIDs':character_ids, 'taleIDs':tale_ids, 'taleFreqs':tale_freqs})
        relation_element.text = str(character_combination)
        relation_elements.append(relation_element)

    tales_node.extend(tale_elements)
    sentences_node.extend(sentence_elements)
    tokens_node.extend(token_elements)
    lemmas_node.extend(lemma_elements)
    tags_node.extend(tag_elements)
    characters_node.extend(character_elements)
    relations_node.extend(relation_elements)

    doc = prettify(root_node)
    with open('tales_neo4j.tcf.xml', 'w') as f:
        f.write(doc)

if __name__ == "__main__":
    tcf_file = TCF_File()
    #write_stats(tcf_file)
    characters = ['König', 'Fuchs', 'Königin', 'Wolf', 'Königstochter', 'Jäger']
    explore_list = explore_relations(tcf_file, characters)
    construct_new_tree(tcf_file, explore_list)