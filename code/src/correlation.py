import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

import time

from HandleGenre import apriori
from HandleGenre import deleteGenre
import csv
from enum import Enum

	
client = MongoClient()

db = client.jam_database
track = db.tracks
jam = db.jams
user_gener=db.user_gener

geners = apriori("127.0.0.1", 27017,"temp_database", "tracks", "artist_terms", 0.1)
user_gener={}
gener_user={}

def get_tracks(title,artist):
	artist_terms=[]
	for collection in db.tracks.find({'artist_name':artist,'title':title}):
		artist_terms=collection['artist_terms']
		return artist_terms
	return artist_terms

		

def get_data():
	counter=0
	user_id={}
	start_time=time.time()
	
	
	count=0
	counte=0
	gener_user={}
	
	for collection in jam.find():
		user_id[collection['title']]=0
		
	print len(user_id)
			
	for gener in geners:
			gener_user[gener]=0
	
	#for key,value in user_id.items():
	#	user_gener[key]=gener_user
		#print user_gener
	
	'''for key,value in user_id.items():
		temp=key
		
		user_gener.get(key).get('folk')=
		print a
		break
	print user_gener.get(temp)'''
	
	print("--- %s seconds ---" % (time.time() - start_time))
	

	start_time=time.time()
	countere=0
	counter=0
	counter3 =0
	for jams in jam.find():    ##This will give the songs listned by a particular user
		counter3 = counter3 + 1
		artist_terms=[]
		artist=jams['artist'].strip()
		title=jams['jam_id'].strip()
		
		artist_terms = get_tracks(title,artist)
			
		if len(artist_terms) != 0:
			userId = jams['title']
			if user_gener.has_key(userId)!=None:
				tmp_gnr = {}
				for gener in geners:
					tmp_gnr[gener]=0
				user_gener[userId]=tmp_gnr
			countere= countere+1
			tmp = user_gener.get(userId)
			for term in artist_terms: 			##Loop throught the artist song geners and increment the counter
				try:
					tmp[term] = tmp.get(term) + 1
				except:
					counter=counter+1
			user_gener[userId] = tmp
		
		if countere == 2:
			break
			
	print counter3
	#print user_gener
	
	for key,value in user_gener.items():
		mongo_data={}
		mongo_data['user_id']=key
		mongo_data['track']=value
		result = db.user_gener.insert_one(mongo_data)
		print result

	print("--- %s seconds ---" % (time.time() - start_time))
	
def main():
	get_data()
	
main()	





