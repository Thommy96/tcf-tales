# tcf-tales
Authors: Thomas Bott, Sebastian Sammet
## Project of Text Technology
This Repository contains scripts and files for the project of the course Text Technology WS 20/21 at the IMS, University of Stuttgart.

## Worflow
You can run the main.py to collect and prepare the tcf xml file.
You have to specifiy a list of characters you want to investigate in a txt file with one character per line. For testing you can use the test_characters.txt.
E.g. run in the command line: python3 <path_to>/main.py <path_to>/test_characters.txt

### Collect
The tcf xml file is automaticall downloaded in tcf_file.py.
You can find the used corpus here: https://www.deutschestextarchiv.de/book/show/grimm_maerchen01_1857
and download it here: https://www.deutschestextarchiv.de/book/download_fulltcf/32290

Corpus statistics are computed, written to tsv files and plots are generated as png.

### Prepare
Additional annotation layers are added:
- tale boundaries
- characters
- relations between each pair of characters

A new xml file is created (tales_neo4j.tcf.xml) which contains all relevant information and can be used as input for Neo4J.

### Access (+ extension)
You can download and install Neo4J here: https://neo4j.com/try-neo4j/?ref=brb
and find more detailed information regarding the import of xml to Neo4J here: https://neo4j.com/labs/apoc/4.2/import/xml/

Pay attention to the following steps when setting up the DBMS:
- put the xml file (tales_neo4j.tcf.cml) in the import folder of the DBMS
- set apoc.import.file.enabled=true in the config file of the DBMS
- activate the apoc plugin

You can import the xml file and create a graph with the Cypher commands provided in neo4j_import_commands.txt.
You can simply copy & paste all commands at once into the shell.