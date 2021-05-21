from elasticsearch import Elasticsearch
es = Elasticsearch()



print(es.indices.exists("data1"))
es.indices.create(index="data1")
print(es.indices.exists("data1"))



