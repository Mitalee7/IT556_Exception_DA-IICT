ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'lib'
TYPE_NAME = 'books'
ID_FIELD = 'book_id'
import csv
#opening the csv file from where we take our data
with open ('C:\\Users\\Dimple Shah\\Desktop\\mtech\\reco\\book_ds.csv','r') as File:
    csv_file_object = csv.reader(File)
    header = next(csv_file_object)
    header = [item.lower() for item in header]
    bulk_data = []
#reading the line by line data from csv file and adding to bulk data
    for row in csv_file_object:
       # print(row)
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
#creating the object of elasticsearch which will help to create and delete the index and requesting the DSL query
from elasticsearch import Elasticsearch
es = Elasticsearch(hosts = [ES_HOST])
#deleting the index if the index exists
if es.indices.exists(INDEX_NAME):
    print("deleting index... ", INDEX_NAME)
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))
# since we are running locally, use one shard and no replicas
request_body = {
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 0,
#creating the custom analyzer which will use the filter my_stop which will discard the stop words(and,is,the) just like stop analyzer and tockenize the words to lowercase just like the lowercase analyzer do
            "analysis": {
               "filter": {
                "my_stop": {
                    "type": "stop",
                    "stopwords": ["and", "is", "the"]
                            }
                         },
               "analyzer":{
                            "My_analyzer":{
                              "tokenizer":"lowercase",
                                "filter":"my_stop"
                            }
                          }
                        } 

        },
        "mappings": {
            "books": {
                "properties": {
                    "author": {
                        "type": "text",
                        "index_options": "offsets",
#Applying the 'fingerprint' analyzer to the indexing of author field
                        "analyzer":"fingerprint",
#Applying the 'fingerprint' analyzer to the search_mapping on author field
#The fingerprint analyzer is a specialist analyzer which creates a fingerprint which can be used for duplicate detection.
                        "search_analyzer": "fingerprint"
                    },
                "title": {
                        "type": "text",
                        "index_options": "offsets",
#Applying the 'simple' analyzer to the indexing of author field
#The simple analyzer divides text into terms whenever it encounters a character which is not a letter. It lowercases all terms.
                        "analyzer":"simple",
#Applying the 'My_analyzer' analyzer to the search_mapping on author field        
                        "search_analyzer": "My_analyzer"
                    },
                "genre": {
                        "type": "text",
                        "index_options": "offsets",
#Applying the 'keyword' analyzer to the indexing of author field
#The keyword analyzer is a “noop” analyzer that accepts whatever text it is given and outputs the exact same text as a single term.
                        "analyzer":"keyword",
#Applying the 'keyword' analyzer to the search_mapping on author field        
                        "search_analyzer": "keyword"
                    }
                
	        }
            }
        }
        }
print("creating '%s' index..." % ('library'))
res = es.indices.create(index = INDEX_NAME, body = request_body,ignore=400)
print(" response: '%s'" % (res))
print("bulk indexing...")
res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
#DSL query
res = es.search(index = INDEX_NAME,body={"query": {"match": {"author" : "Mike Allision"}}})
#Here we have applied the 'fingerprint' analyzer on both indexing as well as search mapping so it will convert the 'Mike Allision' into 'Allision Mike' and return the matching document 
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])
res = es.search(index = INDEX_NAME,body={"query": {"match": {"title" : "The and Comfort"}}})
#Here we have applied the 'My_analyzer' analyzer on search mapping and  "simple" on indexing  so it will convert the 'The and Comfort' into 'comfort' and return the matching document
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])
res = es.search(index = INDEX_NAME,body={"query": {"match": {"genre" : "Travel and Adventure"}}})
#Here we have applied the 'keyword' analyzer on both indexing as well as search mapping so it will return the exact matching document 
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])
#Here we have applied the 'standard' analyzer on the text so it will divides text into terms on word boundaries and  removes most punctuation, lowercases terms, and supports removing stop words. 
res=es.indices.analyze(body={"text":"this is how the standard analyzer works","analyzer":"standard"})
print(" response: '%s'" % (res))
#Here we have applied the 'simple' analyzer on the text so it will divide text into terms whenever it encounters a character which is not a letter. It lowercases all terms. 
res=es.indices.analyze(body={"text":"this is how the Simple2ANALYZER works","analyzer":"simple"})
print(" response: '%s'" % (res))
#Here we have applied the 'WHITESPACE' analyzer on the text so it will divide text into terms whenever it encounters any whitespace character. It does not lowercase terms. 
res=es.indices.analyze(body={"text":"this is how the WHITESPACE ANALYZER works","analyzer":"whitespace"})
print(" response: '%s'" % (res))
#Here we have applied the 'PATTERN' analyzer on the text so it uses a regular expression to split the text into terms. The regular expression should match the token separators not the tokens themselves. The regular expression defaults to \W+ (or all non-word characters).
res=es.indices.analyze(body={"text":"this's how the pattern ANALYZER works,it has \W+ pattern by default","analyzer":"pattern"})
print(" response: '%s'" % (res))



