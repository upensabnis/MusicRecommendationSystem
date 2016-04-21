import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

import time
import random
import numpy
import itertools
import operator
from HandleGenre import apriori
from HandleGenre import deleteGenre

client = MongoClient()

db = client.jam_database
track = db.tracks
jam = db.jams
cluster=db.cluster

cluster_data={}
cluster_users=[]
cluster_selection=2
user_songs={}

start_time=time.time()

for data in cluster.find():
	cluster_data[data['cluster']]=data['users']

cluster_users=cluster_data[cluster_selection]
#print cluster_users

titles=[]
artist=[]
usertosongs={}

for user in cluster_users:
	usertosongs[user]=[]
	for data in jam.find({'title':user}):
		usertosongs[user].append('jam_id')

for user in cluster_users:			#This will get all the songs listen by each user in the cluster
	for data in jam.find({'title':user}):
		titles.append(data['jam_id'])
		artist.append(data['artist'])

print len(titles),len(artist)
		
songs_count={}

for title in titles:
	songs_count[title]=0

for title,artist in zip(titles,artist): #This will get the matching song from the tracks tables
	for data in track.find({'title':title,'artist_name':artist}):
		songs_count[title]=songs_count[title]+1

final_songs={}
for key,value in songs_count.items():
	if value!=0:
		final_songs[key]=value
		
print final_songs



			

	
print("--- %s seconds ---" % (time.time() - start_time))	
	
	
	
	
	
	
	
	
	
	
	



