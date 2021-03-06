# Overview
Authors: Thomas Bott, Sebastian Sammet
## Content of this overview
This overview contains information about the enclosed query results. These results were generated with Neo4j in the framework of our Text Technology project called tcf-tales. It contains data about relations between nouns in a collection of fairy tales.
## Motivation
As we investigated the relations between nouns we ran into a problem: There are many different nouns and appart from the most frequent ones the relations between them were hard to research. In an effort to make the relations more clear we created categories and put those nouns in categories, that fit and were frequent (in the file ``top50_plus_top10Tales_nouns.txt``).
### Categories
First and foremost in our resarch of relations between nouns we wanted to investigate especially characters, but as research continued other nouns also catched our interests. So we came up with 12 Categories:

Category | English | Description if necessary
-------- | -------- | --------
Adel   | Nobility|Any title that denotes nobility
Tier   |Animal    
Fabelwesen |Mythical Creature| Creatures belonging to the realms of myths
Männlich |Male|Any noun that is explicitely male
Weiblich |Female|Any noun that is explicitely female
Gewerbebezeichnung |Profession Title| Any noun telling what a person does for a living
Wertgegenstände |Valuables|Items or materials that are considered valuable
Orte      |Places|
Eigenname    |Proper Name|
Beziehung    |Relation|A noun that implies a relation to someone else
Nahrung     |Food|
Körperteil    |Body Part|

The categories "Weiblich" and "Männlich" have some overlap with "Adel", "Gewerbebezeichnung" and "Beziehung".
### Queries
After we sorted out the categories we wrote queries for Neo4j to investigate the relations between our noun categories. The corresponding queries are found in ``cypher_queries.txt``. Our project also contains some results, which are in .csv and .png-Format.
