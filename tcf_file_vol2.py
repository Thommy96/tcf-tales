"""
@author: Thomas Bott
@author: Sebastian Sammet
"""
import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen

class TCF_File_vol2:
    """
    This class is used to parse a XML file in TCF format and save all its information (annotation layers, elements, ...).
    Furthermore tale boundaries are reconstructed and annotated.
    """

    def __init__(self) -> None:
        """Ititialize a tcf object, i.e. search the xml document with xpath queries and store information in dictionaries

        Args:
            tcf_path (str): path to the tcf xml file
        """
        tcf_url = urlopen('https://www.deutschestextarchiv.de/book/download_fulltcf/32290')
        tcf_url_vol2 = urlopen('https://www.deutschestextarchiv.de/book/download_fulltcf/32296')
        self.tree = ET.parse(tcf_url)
        self.tree_vol2 = ET.parse(tcf_url_vol2)

        self.tokens = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}tokens")[0]
        self.tokens_vol2 = self.tree_vol2.findall(
                        ".//{http://www.dspin.de/data/textcorpus}tokens")[0]
        self.tokens_dict = {}
        for token in self.tokens:
            token_id = token.attrib["ID"]
            token_value = token.text
            self.tokens_dict[token_id] = token_value
        for token in self.tokens_vol2:
            token_id = token.attrib["ID"] + '_vol2'
            token_value = token.text
            self.tokens_dict[token_id] = token_value

        self.lemmas = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}lemmas")[0]
        self.lemmas_vol2 = self.tree_vol2.findall(
                        ".//{http://www.dspin.de/data/textcorpus}lemmas")[0]
        self.lemmas_dict = {}
        for lemma in self.lemmas:
            token_id = lemma.attrib["tokenIDs"]
            lemma_value = lemma.text
            self.lemmas_dict[token_id] = lemma_value
        for lemma in self.lemmas_vol2:
            token_id = lemma.attrib["tokenIDs"] + '_vol2'
            lemma_value = lemma.text
            self.lemmas_dict[token_id] = lemma_value

        self.POStags = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}POStags")[0]
        self.POStags_vol2 = self.tree_vol2.findall(
                        ".//{http://www.dspin.de/data/textcorpus}POStags")[0]
        self.pos_dict = {}
        for pos in self.POStags:
            token_id = pos.attrib["tokenIDs"]
            pos_value = pos.text
            self.pos_dict[token_id] = pos_value
        for pos in self.POStags_vol2:
            token_id = pos.attrib["tokenIDs"] + '_vol2'
            pos_value = pos.text
            self.pos_dict[token_id] = pos_value

        self.sentences = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}sentences")[0]
        self.sentences_vol2 = self.tree_vol2.findall(
                        ".//{http://www.dspin.de/data/textcorpus}sentences")[0]
        self.sentences_dict = {}
        for sentence in self.sentences:
            sentence_id = sentence.attrib["ID"]
            token_ids = sentence.attrib["tokenIDs"].split()
            self.sentences_dict[sentence_id] = token_ids
        for sentence in self.sentences_vol2:
            sentence_id = sentence.attrib["ID"] + '_vol2'
            token_ids = sentence.attrib["tokenIDs"].split()
            token_ids = [id + '_vol2' for id in token_ids]
            self.sentences_dict[sentence_id] = token_ids

        self.orthography = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}orthography")[0]
        self.orthography_vol2 = self.tree_vol2.findall(
                        ".//{http://www.dspin.de/data/textcorpus}orthography")[0]
        self.corrections_dict = {}
        for correction in self.orthography:
            token_id = correction.attrib["tokenIDs"]
            correction_value = correction.text
            self.corrections_dict[token_id] = correction_value
        for correction in self.orthography_vol2:
            token_id = correction.attrib["tokenIDs"] + '_vol2'
            correction_value = correction.text
            self.corrections_dict[token_id] = correction_value
        
        self.tales_dict = self.get_tales()

    def get_tales(self) -> dict:
        """This function constructs the tales dict by assigning all corresponding sentence ids for each tale.

        Returns:
            dict: taleID, sentenceIDs
        """
        tales_titles_ids = self.get_tales_title_ids()
        tale_sentence_ids = []
        tales_dict = {}
        id_counter = 0
        for sentence_id, token_ids in self.sentences_dict.items():
            if sentence_id in tales_titles_ids:
                if sentence_id == tales_titles_ids[0] or sentence_id == tales_titles_ids[86]:
                    #this is the start of the first tale, don't add the Vorwort to tales_dict
                    tale_sentence_ids = []
                    if sentence_id not in tale_sentence_ids:
                        tale_sentence_ids.append(sentence_id)
                else:
                    # a new tale starts here, add collected sentence ids to tales_dict and reset tale_sentence_ids
                    tale_id = "t" + str(id_counter)
                    id_counter += 1
                    tales_dict[tale_id] = tale_sentence_ids
                    tale_sentence_ids = []
                    if sentence_id not in tale_sentence_ids:
                        tale_sentence_ids.append(sentence_id)
            if sentence_id == "s10c3" or sentence_id == "s11d1_vol2":
                # this is the last sentence of the corpus, needed to add the last tale to tales_dict
                tale_sentence_ids.append(sentence_id)
                tale_id = "t" + str(id_counter)
                id_counter += 1
                tales_dict[tale_id] = tale_sentence_ids
                tale_sentence_ids = []
            else:
                if sentence_id not in tale_sentence_ids:
                        tale_sentence_ids.append(sentence_id)
        return tales_dict

    def get_tales_title_ids(self) -> list:
        """This function finds all tale title ids

        Returns:
            list: tale title ids
        """
        tales_titles_ids = []
        tales_titles_ids_vol2 = []
        for sentence_id, token_ids in self.sentences_dict.items():
            sentence = self.get_sentence(sentence_id)
            first_word = sentence[0].split('.')[0]
            try:
                number = int(first_word)
            except:
                number = 999
                pass
            if number in range(87):
                tales_titles_ids.append(sentence_id)
            if number in range(87,201):
                tales_titles_ids_vol2.append(sentence_id)
        tales_titles_ids = tales_titles_ids[86:172]
        tales_titles_ids_vol2 = tales_titles_ids_vol2[115:]
        tales_titles_ids += tales_titles_ids_vol2
        return tales_titles_ids

    def get_sentence(self, sentence_id:str) -> list:
        """This function returns the corrsponding sentence as a list of token for a sentence id

        Args:
            sentence_id (str): sentence id

        Returns:
            list: list of token of the sentence
        """
        token_ids = self.sentences_dict[sentence_id]
        sentence = []
        for token_id in token_ids:
            token = self.tokens_dict[token_id]
            sentence.append(token)
        return sentence