ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'library'
TYPE_NAME = 'book'
ID_FIELD = 'book_id'
from elasticsearch import Elasticsearch
# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])
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
