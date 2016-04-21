import os
import time
from pymongo import MongoClient

client = MongoClient()


db = client.temp_database
tracks = db.tracks
jams = db.jams

def get_tracks(title,artist):
	artist_terms=[]
	#print title,artist
	for collection in db.tracks.find({'artist_name':artist,'title':title}):
		artist_terms=collection['artist_terms']
		return artist_terms
	return artist_terms
	
if __name__== "__main__":
	trackCountDict = {}
	
	for j in jams.find().limit(100000):
		u_id = j['user_id']
		title = j['title']
		artist = j['artist']	
		#tracks.find({'title':title,'artist_name':artist}).count()
		
		for t in tracks.find({'title':title,'artist_name':artist}):
		#if t.count() > 0:	
			#print 
			ttl = t['title']
			artst = t['artist_name']
			tid = t['track_id']
			count = 0
			userDict = {}
			
			if (title == ttl and artist == artst):
				print 'matched'
				print title
				print artist
				if trackCountDict.has_key(u_id) == False:					
					trackCountDict[u_id] = userDict

				if trackCountDict[u_id].has_key(tid) == False:
					trackCountDict[u_id][tid] = 1
				else:
					uDict = trackCountDict.get(u_id)
					uDict[tid] = uDict[tid] + 1
			break
		
	print trackCountDict
				#print u_id1
				#print title1
				#print artist1
				#print '\n'
