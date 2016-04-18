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

db = client.temp_database
track = db.tracks
jam = db.jams
user_gener=db.user_gener

geners = apriori("127.0.0.1", 27017,"temp_database", "tracks", "artist_terms", 0.1)


def get_tracks(title,artist):
	artist_terms=[]
	for collection in db.tracks.find({'artist_name':artist,'title':title}):
		print title,artist
		print type(collection['artist_terms'])
		artist_terms=collection['artist_terms']
		return artist_terms
	return artist_terms

		

def get_data():
	counter=0
	user_id={}
	start_time=time.time()
	
	artist_terms=[]
	count=0
	for collection in jam.find():
		user_id[collection['title']]=0
		count=count+1
		if len(user_id) == 50:
			break
		
	print len(user_id)
	
	print("--- %s seconds ---" % (time.time() - start_time))
	
	start_time=time.time()
	for key,value in user_id.items():   #loop through the whole user list
		user_geners={}
		sum_geners=0
		user_geners['user_id']=key
		
		for gener in geners:
			user_geners[gener]=0
			
		for jams in jam.find({'title':key}):    ##This will give the songs listned by a particular user
			#print jams['artist'],jams['jam_id']
			artist=jams['artist'].strip()
			title=jams['jam_id'].strip()
			artist_terms = get_tracks(title,artist)
			if type(artist_terms)!=None:
				for term in artist_terms: 			##Loop throught the artist song geners and increment the counter
					try:
						user_geners[term]=user_geners[term]+1
					except:
						counter=counter+1
		
		for gener in geners:
			sum_geners=sum_geners+user_geners[gener]	
		
		if sum_geners != 0:
			result = db.user_gener.insert_one(user_geners)
			print result
			print user_geners
		
		
	print("--- %s seconds ---" % (time.time() - start_time))
	
	
	
def main():
	get_data()
	
main()	





