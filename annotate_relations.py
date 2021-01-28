import itertools
from xml.dom import minidom
from tcf_file import TCF_File
import xml.etree.ElementTree as ET

class Annotation:

    def __init__(self, tcf_file:TCF_File, characters:list):
        self.tcf_file = tcf_file
        self.characters = characters
        self.charcter_freqs_total, self.character_freqs_tales, self.relation_freqs_total, self.relation_freqs_tales = self.explore_relations()

    def explore_relations(self):
        character_combinations = list(itertools.combinations(self.characters, 2))
        character_freqs_total = {}
        character_freqs_tales = {}
        relation_freqs_total = {}
        relation_freqs_tales = {}

        for tale_id, sentence_ids in self.tcf_file.tales_dict.items():
            for sentence_id in sentence_ids:
                sentence_lemmas = []
                for token_id in self.tcf_file.sentences_dict[sentence_id]:
                    lemma = self.tcf_file.lemmas_dict[token_id]
                    sentence_lemmas.append(lemma)
                    if lemma in self.characters:
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

    def construct_new_tree(self):
        root_node = ET.Element('TextCorpus')

        comment = ET.Comment('tales without metadata, orthography, Vorwort and namespaces, for easier processing with neo4j')
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

        for tale_id, sentence_ids in self.tcf_file.tales_dict.items():
            #tale
            tale_title = " ".join(self.tcf_file.get_sentence(sentence_ids[0]))
            sentence_ids_string = " ".join(sentence_ids)
            tale_element = ET.Element('tale', {'ID':tale_id, 'title':tale_title, 'sentenceIDs':sentence_ids_string})
            tale_elements.append(tale_element)

            #sentence
            for sentence_id in sentence_ids:
                token_ids = self.tcf_file.sentences_dict[sentence_id]
                token_ids_string = " ".join(token_ids)
                sentence_element = ET.Element('sentence', {'ID':sentence_id, 'tokenIDs':token_ids_string})
                sentence_elements.append(sentence_element)
            
                #token
                for token_id in token_ids:
                    token_element = ET.Element('token', {'ID':token_id})
                    token_element.text = self.tcf_file.tokens_dict[token_id]
                    token_elements.append(token_element)

                    #lemma
                    lemma_element = ET.Element('lemma', {'tokenIDs':token_id})
                    lemma_element.text = self.tcf_file.lemmas_dict[token_id]
                    lemma_elements.append(lemma_element)

                    #tag
                    tag_element = ET.Element('tag', {'tokenIDs':token_id})
                    tag_element.text = self.tcf_file.pos_dict[token_id]
                    tag_elements.append(tag_element)
        
        character_id_dict = {}
        id_counter = 0
        for character, freq in self.charcter_freqs_total.items():
            character_id = 'c' + str(id_counter)
            character_id_dict[character] = character_id
            id_counter += 1
            tale_ids = " ".join(list(self.character_freqs_tales[character].keys()))
            str_freqs = [str(freq) for freq in list(self.character_freqs_tales[character].values())]
            tale_freqs = " ".join(str_freqs)
            character_element = ET.Element('character', {'ID':character_id, 'freq':str(freq), 'taleIDs':tale_ids, 'taleFreqs':tale_freqs})
            character_element.text = character
            character_elements.append(character_element)

        id_counter = 0
        for character_combination, freq in self.relation_freqs_total.items():
            relation_id = 'r' + str(id_counter)
            id_counter += 1
            character_ids = " ".join([character_id_dict[character_combination[0]], character_id_dict[character_combination[1]]])
            tale_ids = " ".join(list(self.relation_freqs_tales[character_combination].keys()))
            str_freqs = [str(freq) for freq in list(self.relation_freqs_tales[character_combination].values())]
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

        doc = self.prettify(root_node)
        with open('tales_neo4j.tcf.xml', 'w') as f:
            f.write(doc)

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")