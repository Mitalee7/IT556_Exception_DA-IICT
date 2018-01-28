import csv
ES_HOST={"host":"localhost","port":9200}
from elasticsearch import Elasticsearch
with open ('C:\\book30-listing-test.csv','r') as File:
    csv_file_object = csv.reader(File)
    header = next(csv_file_object)
    bulk_data = []
    for row in csv_file_object:
        data_dict = {}
        for i in range(len(row)):
            data_dict[header[i]] = row[i]
        op_dict = {
            "index": {
                "_index": 'book',
                "_type": 'medical',
                "_id": data_dict['book_id']
                }      
        }
        bulk_data.append(op_dict)
        bulk_data.append(data_dict)
#create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])
if es.indices.exists('book'):
    print("deleting '%s' index..." % ('book'))
    res = es.indices.delete(index = 'book')
    print(" response: '%s'" % (res))
# since we are running locally, use one shard and no replicas
request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    'mappings':{
        'medical':{
            'properties':{
                "text":{
                    "type":"text",
                    "index_options":"docs"
                }
            }
        }
    }
}

print("creating '%s' index..." % ('book'))
res = es.indices.create(index = 'book', body = request_body)
print(" response: '%s'" % (res))

print("bulk indexing...")
res = es.bulk(index = 'book', body = bulk_data, refresh = True)

print("=============================================================")
print("Boolean Query")

# Display the data where title field must contain Oral and Based
res = es.search(index = 'book',
                body={"query":
                      {"bool":
                       { "must" :
                         { "match" :
                           {"title" : {"query" : "Oral Based" , "operator" : "and"}}
                           }
                         }
                       }
                      }
                )
print(" response: '%s'" % (res))

print("=============================================================")
print("=============================================================")
#Display the data with book type as Law
res = es.search(index = 'book',
                body={"query":
                      {"bool":
                       { "filter" :
                         { "match" :
                           { "type" : "Law"}
                           }
                         }
                       }
                      }
                )
print(" response: '%s'" % (res))


print("=============================================================")
print("=============================================================")


# Display the data with number of sells are  not between 20 and 9

res = es.search(index = 'book',
                body={"query":
                      {"bool":
                       { "must_not" :
                         { "range" :
                           { "num_sells" : { "gte" : 20 , "lte" : 9 } }
                           }
                         }
                       }
                      }
                )
print(" response: '%s'" % (res))

print("=============================================================")
print("=============================================================")

print("Boosting Queries")

# Dispaly the data where book type contains "computer" but also the contains "science" but downgrade it by
# using negative_boost

res = es.search(index = 'book', body={
            "query": {
                        "boosting" : {
                                    "positive" : {
                                        "match" : {
                                            "type": {"query" : "computer" } 
                                        }
                                    },
                                    "negative" : {
                                         "match" : {
                                             "type": {"query" : "science"}
                                           
                                        }
                                    },
                                    "negative_boost" : 0.5
                                }
                        
                      }
                    })
print(" response: '%s'" % (res))

print("=============================================================")
print("=============================================================")

print("Queries related to minimum_should_search")

print("=============================================================")
# Display the data with minimum_should_match as 1
res = es.search(index = 'book', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "num_sells" : 10 } },
                            { "match" : { "author" : "Jay" } },
                            { "match" : { "title" : "ABCV" } }
                          ],
                              "minimum_should_match" : 1
                          
                        }
                      }
                    })
print(" response: '%s'" % (res))

 
print("=============================================================")
print("=============================================================")

# Display the data with minimum_should_match as -1
res = es.search(index = 'book', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "num_sells" : 10 } },
                            { "match" : { "author" : "Jay" } },
                            { "match" : { "title" : "ABCV" } }
                          ],
                              "minimum_should_match" : -1
                          
                        }
                      }
                    })
print(" response: '%s'" % (res))


# Display the data with minimum_should_match as 2
res = es.search(index = 'book', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "num_sells" : 10 } },
                            { "match" : { "author" : "Jay" } },
                            { "match" : { "title" : "ABCV" } }
                          ],
                              "minimum_should_match" : 2
                          
                        }
                      }
                    })
print(" response: '%s'" % (res))

print("=============================================================")
print("=============================================================")


# Display the data with minimum_should_match as 3
res = es.search(index = 'book', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "num_sells" : 10 } },
                            { "match" : { "author" : "Jay" } },
                            { "match" : { "title" : "ABCV" } }
                          ],
                              "minimum_should_match" : 3
                          
                        }
                      }
                    })
print(" response: '%s'" % (res))

 
print("=============================================================")
print("=============================================================")

# Display the data with minimum_should_match as 4
res = es.search(index = 'book', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "num_sells" : 10 } },
                            { "match" : { "author" : "Jay" } },
                            { "match" : { "title" : "ABCV" } }
                          ],
                              "minimum_should_match" : 4
                          
                        }
                      }
                    })
print(" response: '%s'" % (res))








