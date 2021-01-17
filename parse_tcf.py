import xml.etree.ElementTree as ET

class TCF_File:

    def __init__(self):
        self.tree = ET.parse("grimm_maerchen.tcf.xml")
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

    def get_sentence(self, sentence_id):
        token_ids = self.sentences_dict[sentence_id]
        sentence = []
        for token_id in token_ids:
            token = self.tokens_dict[token_id]
            sentence.append(token)
        return sentence
    
    def get_tales_title_ids(self):
        tales_titles_ids = []
        for sentence_id, token_ids in self.sentences_dict.items():
            sentence = self.get_sentence(sentence_id)
            first_word = sentence[0].split('.')[0]
            try:
                number = int(first_word)
            except:
                number = 99
                pass
            if number in range(87):
                tales_titles_ids.append(sentence_id)
        tales_titles_ids = tales_titles_ids[86:]
        return tales_titles_ids


if __name__ == "__main__":
    tcf_file = TCF_File()
    tales_titles_ids = tcf_file.get_tales_title_ids()