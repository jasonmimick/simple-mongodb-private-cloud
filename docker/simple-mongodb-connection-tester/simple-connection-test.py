from pymongo import MongoClient
import sys
import uuid
import time

num_docs = 1000

if not len(sys.argv)>=2:
  print "Usage: test-mongo-connection.py <MongoDB Connection String> <number_docs>"
  sys.exit("No connection string detected.")
  
if len(sys.argv)==3:
  num_docs = int(sys.argv[2])

uri = sys.argv[1]
print "simple-connection-test: testing connection to %s" % uri
temp_db_name = "test-%s" % str(uuid.uuid4())[:8]
print "Creating and reading 100 docs in the '%s.foo' namespace" % temp_db_name
#uri = "mongodb+srv://newyork-service.mongodb.svc.cluster.local/?ssl=false"
client = MongoClient(uri)
print client[temp_db_name]
for i in range(0,num_docs):
  client[temp_db_name]['foo'].insert_one( { "i" : i } )
for doc in client[temp_db_name]['foo'].find():
  print doc
client.drop_database(temp_db_name)
print "Dropped db '%s'" % temp_db_name
