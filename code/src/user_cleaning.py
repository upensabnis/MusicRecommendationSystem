import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

client = MongoClient()


db = client.temp_database
collections = db.jams
collections1= db.likes
song_count=0
user_count={}
count=0
users=[]
tracks={}
start_time = time.time()

for collection in collections1.find():
	tracks[collection['artist_name']]=[]
print 'artist added'
for collection in collections1.find():
	tracks[collection['artist_name']].append(collection['title'])
print 'songs dictnory done'

for collection in collections.find(): 
	try:
		print tracks[collection['artist']].index(collection['jam_id'])
	except:
		db.collections.remove({'_id':collection['_id']})
		count = count+1
		
	
print count
print("--- %s seconds ---" % (time.time() - start_time))

