ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'library'
from elasticsearch import Elasticsearch
# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

print("=============================================================")
print("Match all query")
res = es.search(index = INDEX_NAME,body={"query": {"match_all": {}}})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])

print("=============================================================")
print("Query to fetch records with word 'Law'")
res = es.search(index = INDEX_NAME,body={"query": {"match": {"type" : "Law"}}})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])

print("=============================================================")
print("Query to fetch records with word 'Martian' in fields 'title' or 'author'")
res = es.search(index = INDEX_NAME,body={"query": {"multi_match": {"query" : "Martian" , "fields" : ["title","author"]}}})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])

print("=============================================================")
print("Query to fetch records with string 'Martians'")
res = es.search(index = INDEX_NAME,body={"query": {"query_string": {"query" : "Martian"}}})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])

print("=============================================================")
print("query to fetch records which have number of sells greater than 10")
res = es.search(index = INDEX_NAME, body={"query":{"range":{"num_sells":{"gte":10}}}})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])
