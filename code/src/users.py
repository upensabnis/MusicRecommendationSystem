import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

client = MongoClient()


db = client.database_jam
collections = db.jams

song_count=0
user_count={}
count=0
users=[]

start_time = time.time()

for collection in collections.find():
	users.append(collection['title'])
	
for user in users:
	user_count[user]=0

for user in users:
	user_count[user] = user_count[user]+1
	
v=list(user_count.values())
k=list(user_count.keys())

print user_count
print min(v), max(v), len(k)

print("--- %s seconds ---" % (time.time() - start_time))
