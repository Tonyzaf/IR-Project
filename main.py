import csv  
import json  
from pprint import pprint
import urllib
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.serializer import JSONSerializer
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#Connect to elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#Test connection to local server
if es.ping():print('connection success!')
else:print('ping failed')
 
name = raw_input('Insert The Title Of The Movie:\n')

query_body = {
  "query": {
    "bool": {
      "must": {
        "match": {      
          "title": name
        }
      }
    }
  }
}

result = es.search(index="movies", body=query_body,size=999)
all_hits = result['hits']['hits']


print ("total hits:", len(result["hits"]["hits"]))

for num, doc in enumerate(all_hits):
    print ("DOC ID:", doc["_id"], "--->", doc, type(doc), "\n")
    for key, value in doc.items():
        print (key, "-->", value)
    print ("\n\n")