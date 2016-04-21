import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

import time

from HandleGenre import apriori
from HandleGenre import deleteGenre
#import csv
#from enum import Enum

	
client = MongoClient()

db = client.music_database
jam = db.dec_jams
track = db.c_tracks
user_gener=db.user_gener

geners = apriori("127.0.0.1", 27017,"music_database", "c_tracks", "artist_terms", 0.1)
user_gener={}
gener_user={}

def get_tracks(title,artist):
	artist_terms=[]
	#print title,artist
	for collection in track.find({'artist_name':artist,'title':title},no_cursor_timeout=True):
		artist_terms=collection['artist_terms']
		return artist_terms
	return artist_terms

		

def get_data():
	counter=0
	user_id={}
	fo = open('corelation-outputs', 'w')
	start_time=time.time()
	
	
	count=0
	counte=0
	gener_user={}
	
	#for collection in jam.find():
	#	user_id[collection['title']]=0
		
	#print len(user_id)
			
	#for gener in geners:
	#		gener_user[gener]=0
	
	#print("--- %s seconds ---" % (time.time() - start_time))
	

	start_time=time.time()
	countere=0
	counter=0
	counter3 =0
	track_artists = {}
	for collection in track.find({},no_cursor_timeout=True):
		newKey = collection['artist_name'].join(':').join(collection['title'])
		track_artists[newKey] = collection['artist_terms']
		
	for jams in jam.find({},no_cursor_timeout=True):    ##This will give the songs listned by a particular user
		counter3 = counter3 + 1
		artist_terms=[]
		artist=jams['artist'].strip()
		title=jams['jam_id'].strip()
		
		#artist_terms = get_tracks(title,artist)
		searchKey = artist.join(':').join(title)
		artist_terms = track_artists.get(searchKey)	
		
		if artist_terms != None:
			if len(artist_terms) != 0:
				#print artist,title
				userId = jams['title']
				if user_gener.has_key(userId)==False:
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
		
		#if counter3==1000:
			#break
		
			
		if counter3%10000==0:
			print counter3
				
	print counter3
	#print user_gener
	
	for key,value in user_gener.items():
		mongo_data={}
		mongo_data['user_id']=key
		mongo_data['track']=value
		result = db.user_gener.insert_one(mongo_data)
		#print result

	t_required = time.time() - start_time
	fo.write(str(t_required))
	fo.close()
	print("--- %s seconds ---" % (time.time() - start_time))
	
def main():
	get_data()
	
main()	