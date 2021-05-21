

#-------------- Creating a web Indexer-----------
# Two main types of indexes:
#   1--Forward index
#   2--Inverted index

#--------Forward index--------:
#Doc1 =>{yassin, python , ....}
#Doc2 =>{serach, flask, engine,.....}

#-------Inverted index---------:
#yassin =>{doc 1, doc2,do100,....}
#python =>{doc5, doc1,doc25,.....}

#--------------fin------------------------------------

from crawler import parse_text
import json
import argparse
import os.path
class Index():
    def __init__(self):
        self.inverted_index = dict()
        self.forward_index  = dict()
        self.url_to_id      = dict()
        self.doc_count      = 0
    
    def add_document(self, url, parse_text):
        self.doc_count += 1
        assert url not in self.url_to_id
        self.url_to_id = self.url_to_id
        current_id = self.url_to_id
        self.forward_index[current_id] = parse_text #parse text to a list of words
        for word in parse_text:
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word] = []
    
    def store_on_disk(self, index_dir):
        def dump_json_to_file(source, file_name):
            file_path = os.path.join(index_dir, file_name)
            with open(file_path, 'w') as f:
                json.dump(source, f, indent=4)
        dump_json_to_file(self.inverted_index, "inverted_index")
        dump_json_to_file(self.forward_index, "forward_index")
        dump_json_to_file(self.url_to_id, "url_to_id")

class Searcher(object):
    def __init__(self, index_dir):
        self.inverted_index = dict()
        self.forward_index  = dict()
        self.url_to_id      = dict()
        def load_json_from_file(source, file_name):
            file_path = os.path.join(index_dir, file_name)
            with open(file_path) as f:
                json.load(source, f)
        load_json_from_file(self.inverted_index, "inverted_index")
        load_json_from_file(self.forward_index, "forward_index")
        load_json_from_file(self.url_to_id, "url_to_id")

        
        # query has a list of words [word1, word2, ...] => reurns all documents that content one of these words
    def find_documents(self, list_of_words):
        return sum([self.inverted_index[word] for word in list_of_words])

    
    def create_index_from_dir(stored_document_dir, index_dir):
        indexer = Index()
        for file_name in os.Listdir(stored_document_dir):
            opned_file = open(os.path.join(stored_document_dir, file_name))
            parsed_doc = parse_text(opned_file.read()).split(" ")


def main():
    parser = argparse.ArgumentParser(description='Index /r/learnprogramming')
    parser.add_argument("--stored_documents_dir", dest="stored_documents_dir", required=True)
    parser.add_argument("--index_dir", dest="index_dir", required=True)
    args = parser.parse_args()
    #create_index_from_dir_API(args.stored_documents_dir, args.index_dir)


if __name__ == "__main__":
    main()