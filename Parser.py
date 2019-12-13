import csv  
import json  
from pprint import pprint
import requests
import urllib
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.serializer import JSONSerializer
import os,sys

# Open the CSV  
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
#Connect to elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#Test connection to local server
if es.ping():print('success!')
else:print('ping failed')
#import into elasticsearch
MyFile= json.load('movies.json','r')
ClearData = MyFile.splitlines(True)
i=0
json_str=""
docs ={}
for line in ClearData:
    line = ''.join(line.split())
    if line != "},":
        json_str = json_str+line
    else:
        docs[i]=json_str+"}"
        json_str=""
        print (docs[i])
        es.index(index='test', doc_type='Blog', id=i, body=docs[i])
        i=i+1