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

from elasticsearch.client import Elasticsearch
from crawler import parse_text
import json
import argparse
from elastic import index_data
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
    
    def store_on_elastic(self, index_dir):
        es = Elasticsearch()
        es.index(index="inverted_index", doc_type="inverted_index" , body=json.dumps(self.inverted_index))
        es.index(index="forward_index", doc_type="forward_index" , body=json.dumps(self.forward_index))
        es.index(index="url_to_id", doc_type="url_to_id" , body=json.dumps(self.url_to_id))

    

class Searcher(object):
    def __init__(self, index_dir):
        self.inverted_index = dict()
        self.forward_index  = dict()
        self.url_to_id      = dict()

        def load_json_from_elastic():
            es = Elasticsearch()
            self.inverted_index=json.loads(es.get(index="inverted_index", doc_type="inverted_index",id=5))
            self.forward_index=json.loads(es.get(index="forward_index", doc_type="forward_index",id=5))
            self.url_to_id=json.loads(es.get(index="url_to_id", doc_type="url_to_id",id=5))

    # query has a list of words [word1, word2, ...] => reurns all documents that content one of these words
    def find_documents(self, list_of_words):
        return sum([self.inverted_index[word] for word in list_of_words])

    
    def create_index_from_dir(stored_document_dir, index_name):
        indexer = Index()
        es = Elasticsearch()
        all_docs= es.search(index=index_name, doc_type=index_name, body={
            'size':10000,
            'query':{
                    'match_all':{}
            }
        })
        for doc in all_docs:
            parsed_titles  = doc['title'].split(" ")#list of words that exists in all the titles
            parsed_headers = doc['headers'].split(" ")#and also the headers
            parsed_content = doc['content'].split(" ")#....


def main():
    parser = argparse.ArgumentParser(description='Index /r/learnprogramming')
    parser.add_argument("--stored_documents_dir", dest="stored_documents_dir", required=True)
    parser.add_argument("--index_dir", dest="index_dir", required=True)
    args = parser.parse_args()
    #create_index_from_dir_API(args.stored_documents_dir, args.index_dir)


if __name__ == "__main__":
    main()