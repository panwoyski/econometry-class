import bibtexparser
import sys
import json
import sqlite3


class Record(object):
    def __init__(self, dct):
        self.source_dict = dct
        self.ID = dct["ID"]
        self.abstract = self._clear_newlines(dct["abstract"])
        self.author = dct["author"]
        self.cited_references = self._split_citations(dct.get("cited-references", 'no_cited_references'))
        self.doi = dct.get("doi", 'no_doi')
        self.issn = dct["issn"]
        self.journal = dct["journal"]
        self.keyword = dct.get("keyword", 'no_keywords')
        self.language = dct["language"]
        self.number = dct["number"]
        self.pages = dct["pages"]
        self.publisher = dct["publisher"]
        self.research_areas = dct["research-areas"]
        self.title = self._clear_newlines(dct["title"])
        self.type = dct["type"]
        self.unique_id = dct["unique-id"]
        self.volume = dct["volume"]
        self.web_of_science_categories = self._split_categories(dct["web-of-science-categories"])
        self.year = dct["year"]

        self.is_relevant = False

    @property

    @staticmethod
    def _clear_newlines(abstract_str):
        return abstract_str.replace('\n', ' ')

    @staticmethod
    def _split_citations(references_str):
        return references_str.split(sep='\n')

    @staticmethod
    def _split_categories(categories_str):
        return set(categories_str.split(sep='; '))


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
    bib_path = sys.argv[1]
    with open(bib_path, 'r') as bibfile:
        bibtex_str = bibfile.read()

    bib_database = bibtexparser.loads(bibtex_str)

    records = [Record(entry) for entry in bib_database.entries]
    [print(record.title) for record in records]

if __name__ == '__main__':
    main()
