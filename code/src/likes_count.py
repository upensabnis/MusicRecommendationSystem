import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

client = MongoClient()


db = client.temp_database
collections = db.jams
collections1= db.likes

user_count={}
count=0
users=[]
tracks={}
start_time = time.time()

for collection in collections.find():
	tracks[collection['user_id']]=0

print("--- %s seconds ---" % (time.time() - start_time))
print 'users added'

start_time = time.time()
for collection in collections1.find():
	try:
		tracks[collection['jam_id']] = tracks[collection['jam_id']]+1
	except:
		count=count+1

v=list(tracks.values())
k=list(tracks.keys())

print tracks
print count
print min(v), max(v), len(k)

print("--- %s seconds ---" % (time.time() - start_time))

