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

"""The default_field uses the BM25 similarity.

The classic_field uses the classic similarity (ie TF/IDF).

The boolean_sim_field uses the boolean similarity. """
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
                    },
	"default_field": { 
          "type": "text"
        },
        "classic_field": {
          "type": "text",
          "similarity": "classic" 
        },
        "boolean_sim_field": {
          "type": "text",
          "similarity": "boolean" 
        }
	        }
            }
        }
    }
print("creating '%s' index..." % ('library'))
res = es.indices.create(index = 'library', body = request_body)
print(" response: '%s'" % (res))
