import json
from typing import List
from bs4 import BeautifulSoup
import requests
import re
from elasticsearch import Elasticsearch
import uuid
import jsonpickle

class A(object):
    def __init__(self, name):
        self.name=name
def index_links(links,index_name, url):
    data=jsonpickle.encode(A(links))
    es = Elasticsearch('http://127.0.0.1:9200') 
    es.index(index=index_name, doc_type="page_content",id=url, body=data)

def index_data(data, url):
        es = Elasticsearch('http://127.0.0.1:9200') 
        es.index(index="data", doc_type="page_content",id=url, body=json.dumps(data)) 

links = set()
urls = list(links)
def scrap_data(url):
    try:
        req = requests.get(url)
    except:
        print('status code not ok')
    soup = BeautifulSoup(req.text, 'html.parser')

    headers = ''
        #find all tags start with h and have a dih=gital after it and end in the end
    for header in soup.find_all(re.compile('^h[1-6]$')):
            headers = headers+' '+header.text.strip()
    pa= ''
    for p in soup.find_all('p'):
            pa= pa+' '+p.text.strip()

    for link in soup.find_all('a'):
            links.add(link.get('href'))
    result={
                            'id':url,
                            'title':soup.find('title').text,
                            'headers':headers,
                            'content':pa
            }
    index_data(result,url)

data={
    'id':'bjhdbcjhascsacsa',
    'title':'hello java',
    'headers':'tuto yassin',
    'content':'bla bla bla bla, java ,hello'
}
yassin={
    'id':'yassin',
    'title':'hello python',
    'headers':'tuto yassin',
    'content':'bla bla bla bla, java ,hello'
}
def inverted_index(data):
    inverted_indexD=dict()
    for word in data['title'].split(' '):
        if word not in inverted_indexD:
            inverted_indexD[word]=[]
        if data['id'] not in inverted_indexD[word]:
            inverted_indexD[word].append(data['id'])
    for word in data['headers'].split(' '):
        if word not in inverted_indexD:
            inverted_indexD[word]=[]
        if data['id'] not in inverted_indexD[word]:
            inverted_indexD[word].append(data['id'])
    for word in data['content'].split(' '):
        if word  not in inverted_indexD:
            inverted_indexD[word]=[]
        if data['id'] not in inverted_indexD[word]:
            inverted_indexD[word].append(data['id'])
    return inverted_indexD

#scrap_data('https://www.python.org/download')
#es.indices.create('waitting_links')
#es.indices.create('crawled_links')
#print(es.indices.exists('waitting_links'))
#print(es.indices.exists('crawled_links'))

