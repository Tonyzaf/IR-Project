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
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#Test connection to local server
if es.ping():print('success!')
else:print('ping failed')
#deletes index/testing
es.indices.delete(index='movies', ignore=[400, 404])
es.indices.delete(index='ratings', ignore=[400, 404])
def CreateIndex(indexname,type,files):
    directory = '/mnt/c/Users/Eric/Desktop/IR-Project-master'
    i = 1
    for filename in os.listdir(directory):
        if filename.endswith(files):
            f = open(filename)
            Config_File = f.read()
            # Send the data into es
            es.index(index=indexname, ignore=400, doc_type=type, id=i,body=json.loads(Config_File))
            i = i + 1
def CSV2ES(filename,indexname,type):
    with open(filename) as doc:
        r = csv.DictReader(doc)
        helpers.bulk(es, r, index=indexname, doc_type=type)
CreateIndex('movies','movies','movies.mapping.json')
CSV2ES('movies.csv','movies','movies')
CreateIndex('ratings','ratings','rating.mapping.json')
CSV2ES('ratings.csv','ratings','ratings')