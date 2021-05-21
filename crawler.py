#---------------------this is ours crawler---------------

from elastic import index_data, index_links, inverted_index
import requests
#import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

max_depth=1
def download_page(url):
    headers ={
            'User-Agent':'FPT Searching bot version 0.1'
            }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception("not ok status code {}".format(r.status_code))
    return r.text


def parse_text(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs

crawled_links=set()
waitting_links=[[]]
inverted_indexC=dict()
id=1
index=True
def craw(start_url,depth):
                try:
                    
                        waitting_links=[[start_url,0]]
                        current_page_url = start_url
                        current_page = download_page(current_page_url)
                        #page_name = b85encode(current_page_url.encode('ascii'))
                        print("depth:",depth," we are crawling {}".format(current_page_url))
                        #print(page_name)
                        crawled_links.add(current_page_url)
                        soup = parse_text(current_page)
                        headers = ''
                        #find all tags start with h and have a dih=gital after it and end in the end
                        for header  in soup.find_all(re.compile('^h[1-6]$')):
                                headers = headers+' '+header.text.strip()
                        pa= ''
                        for p in soup.find_all('p'):
                            pa= pa+' '+p.text.strip()

                        for link in soup.find_all('a'):
                            waitting_links.append([link.get('href'),depth+1])
                        result = {
                                'id':start_url,
                                'title':soup.find('title').text,
                                'headers':headers,
                                'content':pa
                        }
                        
                except:
                    result=None

                if result is not None:
                    index_data(result, start_url)
                    inverted_indexC=inverted_index(result)
                all_links = soup.find_all('a')
                for link in all_links:
                            if 'http' not in link:
                                url = urljoin(current_page_url, link.get('href'))
                            if [url,depth+1] not in waitting_links and crawled_links:
                                waitting_links.append([url,depth+1])
                            if url not in crawled_links and depth < max_depth:
                                try:
                                    crawled_links.add(url)
                                    craw(url,depth+1)
                                except:
                                    pass


def main():
    craw('https://java.developpez.com/cours/',1)
    index_links(crawled_links,"crawled_links","14")
    index_links(inverted_indexC,"data1","5") 

if __name__=="__main__":
    main()
