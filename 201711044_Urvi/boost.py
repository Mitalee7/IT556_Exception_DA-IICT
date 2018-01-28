ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'library'
from elasticsearch import Elasticsearch
# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])
print("=============================================================")
print("This Query Uses the boost operator ^ to make term 'Mystery' more relevant than another terms.")
res = es.search(index = INDEX_NAME,body={"query": {
        "match" : {
            "title": {
                "query": "  A Hercule Poirot Mystery^2"
                }
            }
        }})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])

print("=============================================================")
print("In this query title fields will be boosted automatically — count more towards the relevance score — at query time")
res = es.search(index = INDEX_NAME,body={"query": {
        "match" : {
            "title": {
                "query": "French Pastry Murder",
                "boost" : 2
            }
        }
    }})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])
