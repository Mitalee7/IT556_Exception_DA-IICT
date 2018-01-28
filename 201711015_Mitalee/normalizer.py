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
#we created our custom normalizer 'library_normalizer' with character filter and token filter
# we will use character filter 'remove_and' which will map '&' to 'and' and ':' to '-'
# we will use lowercase as token fliter which will convert tokens to lowercase 
request_body = {
    'PUT':{
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
              "char_filter": {
                        "remove_and": {
                          "type": "mapping",
                                "mappings": [
                                            "& =>_and_",
                                            ": => -"
                                            ]
                                 }
                          },
          "normalizer": {
               "library_normalizer": {
                       "type": "custom",
                "char_filter": ["remove_and"],
                     "filter": ["lowercase"]
                                }
                       }
                       }
                      },
        
        'mappings': {
            'book': {
                'properties': {
                    "text": {
                        "type": "text",
                        "normalizer": "library_normalizer"
                    }
	        }
            }
        }
        }
    }
print("creating '%s' index..." % ('library'))
res = es.index(index = 'library',doc_type='post', body = request_body)
print(" response: '%s'" % (res))

#we will map data of csv file using bulk indexing
import csv
with open ('C:\\Users\\DELL\\Downloads\\book_data.csv','r') as File:
    csv_file_object = csv.reader(File)
    header = next(csv_file_object)
    header = [item.lower() for item in header]
    bulk_data = []
    for row in csv_file_object:
        print(row)
        data_dict = {}
        for i in range(len(row)):
            data_dict[header[i]] = row[i]
        op_dict = {
            "index": {
                "_index": INDEX_NAME,
                "_type": TYPE_NAME,
                "_id": data_dict[ID_FIELD]
                }      
        }
        bulk_data.append(op_dict)
        bulk_data.append(data_dict)
print("bulk indexing...")
res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)


