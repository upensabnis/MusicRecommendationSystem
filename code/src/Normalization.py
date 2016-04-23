import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

client = MongoClient()


db = client.temp_database
collections = db.tracks

dic = {}
prev= {}
values={}
Normalized_value=0
min_value={}
max_value={}

start_time = time.time()

fields=[
    "artist_familiarity",
    "artist_hotttnesss",
    "danceability",
    "energy",
    "loudness",
    "song_hotttnesss",
    "tempo"
    ]
		
for field in fields:
	values[field]=[]
	
for collection in collections.find():
	for field in fields:
		values[field].append(collection[field])
	
for field in fields:
	min_value[field]=min(values[field])
	print min_value[field]
	max_value[field]=max(values[field])
	print max_value[field]
	
for collection in collections.find(no_cursor_timeout=True):
	for field in fields:
		try:
			Normalized_value= (((collection[field]-min_value[field])/(max_value[field]-min_value[field]))*(1-(-1)))+(-1)
			result=db.tracks.update_one( {"_id": collection.get("_id")},
                                                 {"$set": {field:Normalized_value}}
											)
			#print result
		except ZeroDivisionError:
			print ""
			
for collection in collections.find():
	print collection
	break
	
print("--- %s seconds ---" % (time.time() - start_time))
		
	
		

