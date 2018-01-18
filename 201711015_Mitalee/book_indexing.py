ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'library'
TYPE_NAME = 'book'
ID_FIELD = 'book_id'

from elasticsearch import Elasticsearch
# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])
if es.indices.exists('library'):
    print("deleting '%s' index..." % ('library'))
    res = es.indices.delete(index = 'library')
    print(" response: '%s'" % (res))
# since we are running locally, use one shard and no replicas
request_body = {
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        'mappings': {
            'book': {
                'properties': {
                    "text": {
                        "type": "text",
                        "index_options": "offsets"
                    }
	        }
            }
        }
    }
print("creating '%s' index..." % ('library'))
res = es.indices.create(index = 'library', body = request_body)
print(" response: '%s'" % (res))


