import os
import time
from pymongo import MongoClient

client = MongoClient()
db = client.temp_database
tracks = db.tracks
jams = db.jams

def get_tracks(title,artist):
	artist_terms=[]
	for collection in db.tracks.find({'artist_name':artist,'title':title}):
		artist_terms=collection['artist_terms']
		return artist_terms
	return artist_terms
	
def merge_title_artist(title, artist):
    return title + ":" + artist
 
if __name__== "__main__":
     trackCountDict = {}
     songDict = {}
     
     cursor = db.tracks.find()
     #print cursor.count()
     for track in cursor:

           try:
               title = str(track.get('title')).strip()
               artist = str(track.get('artist_name')).strip()
           except:
               #print track.get('title')
               #print track.get('artist_name')
               continue
           
           key = merge_title_artist(title, artist)
           if(songDict.has_key(key) == False):
               songDict[key] = track.get('song_id')
     

     for j in jams.find():
           u_id = j['user_id']
           try:
               title = str(j['title'])
               artist = str(j['artist'])
           except:
               continue
           key = merge_title_artist(title, artist)
           if ( songDict.has_key(key) == False):
               continue
           
           userDict = {}
    
           if trackCountDict.has_key(u_id) == False:#song not found				
		      trackCountDict[u_id] = userDict
           
           tid = songDict.get(key)
           if (trackCountDict[u_id].has_key(tid) == False):
			trackCountDict[u_id][tid] = 1
           else:
			uDict = trackCountDict.get(u_id)
			uDict[tid] = uDict[tid] + 1
           
     #print trackCountDict
     count = 0
     for user in trackCountDict.keys():
         songs = trackCountDict.get(user)
         if (len(songs) > 5):
             count = count +1
             #print songs
             print "\n"
     print count
     print len(trackCountDict.keys())