import bibtexparser
import sys
import json


class Record(object):
    def __init__(self, dct):
        self.dict = {
            'relevant': 'not checked',
            'issn': dct.get('issn', ''),
            'doi': dct.get('doi', ''),
            'abstract': dct.get("abstract", '').replace('\n', ' '),
            'author':   dct.get("author", '').replace('\n', ' '),
            'cited_references': dct.get("cited-references", '').replace('\n', '; '),
            'title': self._clear_newlines(dct["title"]),
            'year': dct['year'],
            'categories': dct.get('web-of-science-categories', '')
        }
        self.source_dict = dct
        # try:
        #     self.source_dict = dct
        #     self.abstract = self._clear_newlines(dct["abstract"])
        #     self.cited_references = self._split_citations(dct.get("cited-references", 'no_cited_references'))
        #     self.title = self._clear_newlines(dct["title"])
        #     self.categories = self._split_categories(dct["web-of-science-categories"])
        #     self.year = dct["year"]
        # except:
        #     print(dct['type'])
        #     raise

        self.is_relevant = False

    @staticmethod
    def _clear_newlines(abstract_str):
        return abstract_str.replace('\n', ' ')

    # @staticmethod
    # def _split_citations(references_str):
    #     return references_str.split(sep='\n')
    #
    # @staticmethod
    # def _split_categories(categories_str):
    #     return set(categories_str.split(sep='; '))


# def old_main():
#     bib_path = sys.argv[1]
#     with open(bib_path, 'r') as bibfile:
#         bibtex_str = bibfile.read()
#
#     bib_database = bibtexparser.loads(bibtex_str)
#     # print(bib_path)
#     json_path = bib_path.replace('.bib', '.json')
#     with open(json_path, 'wa') as json_file:
#         json.dump(bib_database.entries, json_file)
#     # for record in bib_database.entries[0:1]:


def get_records(bib_path):

    with open(bib_path, 'r') as bibfile:
        bibtex_str = bibfile.read()

    bib_database = bibtexparser.loads(bibtex_str)

    return [Record(entry) for entry in bib_database.entries]


# def get_all_records(folder):
#     import os
#     files = os.listdir(folder)
#     records = []
#     for file in files:
#         path = '%s/%s' % (folder, file)
#         try:
#             records += get_records(path)
#         except:
#             print(path)
#             raise
#     print(len(records))
#     return records

def transform_file(source_file, destination_file):
    records = get_records(source_file)

    import csv
    with open(destination_file, 'w') as out_file:
        field_names = ['relevant', 'year', 'issn', 'doi', 'author', 'title', 'abstract', 'cited_references', 'categories']
        writer = csv.DictWriter(out_file, fieldnames=field_names, dialect='excel-tab')
        writer.writeheader()
        writer.writerows([record.dict for record in records])


def main():
    source_folder = sys.argv[1]
    dest_folder = sys.argv[2]

    import glob
    files = glob.glob(source_folder + '/*.bib')

    import os
    for file_path in files:
        print(file_path)
        _, filename = os.path.split(file_path)
        dest_filename = filename.replace('.bib', '.csv')
        dest_path = '%s/%s' % (dest_folder, dest_filename)
        # print(dest_path)
        transform_file(file_path, dest_path)


if __name__ == '__main__':
    main()
