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
import importlib
importlib.reload (sys)

#Connect to elasticsearch
es = Elasticsearch(['https://site:a8eea5bd2dae91cdaecb6d4479720e6f@gimli-eu-west-1.searchly.com'])
#Test connection to local server
if es.ping():print('connection success!')
else:print('ping failed')
 
UserID = int(input('Insert Your UserID: '))
print(UserID)
name = input('Insert The Title Of The Movie: ')

movie_query_body = {
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
def RatingSearch(mid):
  avg = 0.0
  i= 1
  res = es.search(index='ratings', body={
  "query": {
    "bool": {
      "must": {
        "match": {      
          "movieId": mid
        }
      }
    }
}
}, size=10)
  with open('results.csv', 'w') as f: 
    for doc in res['hits']['hits']:
        my_dict = doc['_source']
        w = csv.DictWriter(f, my_dict.keys())
        w.writerow(my_dict)
  with open('results.csv', 'r') as f: 
    reader = csv.reader(f)
    for row in reader:
        print('UserID:', row[0] ,'Rating:',  row[2])
def MovieSearch():
  res = es.search(index='movies', body=movie_query_body, size=10)
  with open('results.csv', 'w') as f: 
    for doc in res['hits']['hits']:
        my_dict = doc['_source']
        w = csv.DictWriter(f, my_dict.keys())
        w.writerow(my_dict)
  with open('results.csv', 'r') as f: 
    reader = csv.reader(f)
    for row in reader:
        print('Title:', row[1] ,'ID:', row[0],'Genres:',  row[2])
        mid = row[0]
        RatingSearch(mid)
MovieSearch()