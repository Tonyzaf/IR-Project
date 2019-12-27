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
'''
# Convert CSV to JSON
f = open('movies.csv')  
# Change each fieldname to the appropriate field name. I know, so difficult.  
reader = csv.DictReader( f, fieldnames = ( 'MovieID','Movie Name','Genre' ))  
# Parse the CSV into JSON  
out = json.dumps( [ row for row in reader ] )  
print ("JSON parsed!")  
# Save the JSON  
f = open( 'movies.json', 'w')  
f.write(out)  
print ('JSON saved!')
FilePath = open('movies.json')

'''
#Connect to elasticsearch
es = Elasticsearch(['https://site:a8eea5bd2dae91cdaecb6d4479720e6f@gimli-eu-west-1.searchly.com'])
#Test connection to local server
if es.ping():print('connection success!')
else:print('ping failed')
#deletes index/testing
#es.indices.delete(index='movies', ignore=[400, 404])
#es.indices.delete(index='ratings', ignore=[400, 404])
def CSV2ES(filename,indexname,type):
    with open(filename) as doc:
        r = csv.DictReader(doc)
        helpers.bulk(es, r, index=indexname, doc_type=type)
es.indices.create(index = 'movies')
CSV2ES('movies.csv','movies','movies')
es.indices.create(index = 'ratings')
CSV2ES('ratings.csv','ratings','ratings')