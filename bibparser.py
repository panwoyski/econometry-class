import bibtexparser
import sys
import json
import sqlite3


class Record(object):
    def __init__(self, dct):
        self.ID = dct["ID"]
        self.abstract = dct["abstract"]
        self.author = dct["author"]
        self.raw_cited_references = dct["cited-references"]
        self.doi = dct["doi"]
        self.issn = dct["issn"]
        self.journal = dct["journal"]
        self.keyword = dct["keyword"]
        self.language = dct["language"]
        self.number = dct["number"]
        self.pages = dct["pages"]
        self.publisher = dct["publisher"]
        self.research_areas = dct["research-areas"]
        self.title = dct["title"]
        self.type = dct["type"]
        self.unique_id = dct["unique-id"]
        self.volume = dct["volume"]
        self.raw_web_of_science_categories = dct["web-of-science-categories"]
        self.year = dct["year"]

    def _split_citations(self, references_str):
        pass

    def _prune_newlines(self, input_string):
        pass


def old_main():
    bib_path = sys.argv[1]
    with open(bib_path, 'r') as bibfile:
        bibtex_str = bibfile.read()

    bib_database = bibtexparser.loads(bibtex_str)
    # print(bib_path)
    json_path = bib_path.replace('.bib', '.json')
    with open(json_path, 'wa') as json_file:
        json.dump(bib_database.entries, json_file)
    # for record in bib_database.entries[0:1]:

def main():
    

if __name__ == '__main__':
    main()
