# tcf-tales
Authors: Thomas Bott, Sebastian Sammet
## Project of Text Technology
This Repository contains scripts and files for the project of the course Text Technology WS 20/21 at the IMS, University of Stuttgart.  
For a topic description see: ``tt_project_description_Sammt_Bott.pdf`` and for the slides of our presentation see: ``TCF_Tales_slides.pdf``.
## Workflow
In the following it is described how to run the scripts and generate outputs.  
All outputs except of the xml files (we are not sure if we are allowed to share them here) are already contained in this repository.
### 1. Install requirements
First, you should make sure the required packages are installed by running:
```
pip install -r requirements.txt
```
All imports that are used in the scripts but not mentioned in ``requirements.txt`` are already contained in the python standard library.
### 2. Run Python Scripts
Now you can run ``main.py`` to collect and prepare the tcf xml file.
This function takes 2 arguments and an optional option.
```
Usage:
        main.py <character_file> <category_file> [-v]
    
    Arguments:
        <character_file> = file containing the character which should be processed, format: one character per line
        <category_file> = tsv file containing the categories with the respective nouns, format: one category per column

    Options:
        -v --volume2   include volume 2 of the tales collection (problem: file too large for Neo4j)
```
E.g. run in the command line: 
```
python3 <path_to>/main.py <path_to_character_file> <path_to_category_file>
```
#### Character File
As starting point you can use ``test_characters.txt`` as character file.
After running the script for the first time, a character list is created automatically containing the top 10 most frequent nouns of each tale and the top 50 most frequent nouns over all tales. This character file can then be used to run the script again in order to gain a richer analysis.
#### Category File
You should use ``categories.tsv`` as category file. The top 10 most frequent nouns from each tale and the top 50 most frequent nouns overall of the first volume were manually annotated into different categories. A noun can appear in multiple categories.  
The idea behind this is to analyse relations between concepts of nouns.
#### Option: include the second volume
If you use the option ``--volume2``, the second volume of the tales collection can be included in the analysis. However for the access part, we used only the first volume here due to runtime problems during the import in Neo4j.
Depending on using only the first volume or including the second volume, the outputs of the script are saved in different folders, ``vol1``or ``vol2``.
#### Collect
The tcf xml file is automaticall downloaded in tcf_file.py.  
You can find the used corpus here:  
First volume:  
https://www.deutschestextarchiv.de/book/show/grimm_maerchen01_1857  
download: https://www.deutschestextarchiv.de/book/download_fulltcf/32290  
Second volume:  
https://www.deutschestextarchiv.de/book/show/grimm_maerchen02_1857  
download: https://www.deutschestextarchiv.de/book/download_fulltcf/32296  

Corpus statistics are computed, written to files and plots are generated.
#### Prepare
Additional annotation layers are added:
- tale boundaries
- characters
- relations between each pair of characters
- categories
- relations bewteen each pair of categories

A new xml file ``tales_neo4j.tcf.xml`` is created which contains all relevant information and can be used as input for Neo4j.

### Access (+ extension) with Neo4j
You can download and install Neo4j here: https://neo4j.com/try-neo4j/?ref=brb
and find more detailed information regarding the import of xml to Neo4J here: https://neo4j.com/labs/apoc/4.2/import/xml/

Pay attention to the following steps when setting up the DBMS:
- put the xml file ``tales_neo4j.tcf.cml`` in the import folder of the DBMS
- set 'apoc.import.file.enabled=true' in the config file of the DBMS
- activate the apoc plugin

You can import the xml file and create a graph with the Cypher commands provided in ``neo4j_import_commands.txt``.  
Therefore you can simply copy & paste all commands at once into the shell in Neo4j.

``cypher_queries.txt`` contains several queries that can be used to analyse properties of the graph and answer questions regarding characters/nouns, categories and relations.  
The generated lists and screenshots with corresponding queries can be found in the folder ``query_results`` of this repository.  
The names of the generated files are also included for each corresponding query in ``cypher_queries.txt``.
There you can also find a short overview with more information regarding the categories: ``overview.md``.  
Note: in the graph we only talk about characters while we actually mean characters/nouns since we also analyse nouns other than characters.

You can generate a sorted list of similar tales by running ``similar_tales.py``.
```
Usage:
        similar_tales.py <corpus_stats_file>
    
    Arguments:
        <corpus_stats_file> = corpus stats tsv generated by running main.py, contains the top 10 nouns of each tale
```
The similarity between two tales is measured by the overlap of the top 10 most frequent nouns between them.