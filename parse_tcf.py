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
        
        self.tales_dict = self.get_tales()

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

    def get_tales(self):
        tales_titles_ids = self.get_tales_title_ids()
        tale_sentence_ids = []
        tales_dict = {}
        id_counter = 0
        for sentence_id, token_ids in self.sentences_dict.items():
            if sentence_id in tales_titles_ids:
                if sentence_id == tales_titles_ids[0]:
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
            if sentence_id == "s10c3":
                # this is the last sentence of the corpus, needed to add the last tale to tales_dict
                tale_sentence_ids.append(sentence_id)
                tale_id = "t" + str(id_counter)
                tales_dict[tale_id] = tale_sentence_ids
            else:
                if sentence_id not in tale_sentence_ids:
                        tale_sentence_ids.append(sentence_id)
        return tales_dict
    
    def add_tales_layer(self):
        text_corpus = self.tree.findall(
                        ".//{http://www.dspin.de/data/textcorpus}TextCorpus")[0]
        tales_node = ET.Element("tales")
        for tale_id, sentence_ids in self.tales_dict.items():
            sentence_ids_string = sentence_ids[0]
            for sentence_id in sentence_ids[1:]:
                sentence_ids_string = sentence_ids_string + " " + sentence_id
            sentence_ids_string = sentence_ids_string.strip()
            tale_node = ET.Element("tale", attrib={"ID": tale_id, "sentenceIDs": sentence_ids_string})
            tales_node.append(tale_node)
        text_corpus.append(tales_node)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

if __name__ == "__main__":
    tcf_file = TCF_File()
    tcf_file.add_tales_layer()
    root = tcf_file.tree.getroot()
    indent(root)
    tcf_file.tree.write("test_output.tcf.xml", encoding="utf-8", xml_declaration=True)