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
es = Elasticsearch(['https://site:a8eea5bd2dae91cdaecb6d4479720e6f@gimli-eu-west-1.searchly.com'])
#Test connection to local server
if es.ping():print('connection success!')
else:print('ping failed')
 
UserID = int(input('Insert Your UserID: '))
print(UserID)
name = raw_input('Insert The Title Of The Movie: ')

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
res = es.search(index="movies", body=query_body, size=10)
with open('results.csv', 'w') as f: 
    header_present  = False
    for doc in res['hits']['hits']:
        my_dict = doc['_source'] 
        if not header_present:
            w = csv.DictWriter(f, my_dict.keys())
            w.writeheader()
            header_present = True
        w.writerow(my_dict)
with open('results.csv', 'r') as f: 
    reader = csv.reader(f)
    for row in reader:
      print('Title:', row[2] ,'ID:', row[1],'Genres:',  row[0])