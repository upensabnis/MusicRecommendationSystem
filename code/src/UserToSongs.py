import os
import time
from pymongo import MongoClient

client = MongoClient()
db = client.temp_database
tracks = db.tracks
jams = db.jams
contentTrain = db.contentTrain
contentTest = db.contentTest

def get_tracks(title,artist):
	artist_terms=[]
	for collection in db.tracks.find({'artist_name':artist,'title':title}):
		artist_terms=collection['artist_terms']
		return artist_terms
	return artist_terms
	
def merge_title_artist(title, artist):
    return title + ":" + artist
 
if __name__== "__main__":

     start_time = time.time()
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
           
     testDict = {}
     trainDict = {}
     count = 0
     for user in trackCountDict.keys():
         songs = trackCountDict.get(user)
         train = songs
         if (len(songs.keys()) > 5): # more than 5 songed users
             count = count +1
             num_songs = len(songs.keys())
             slash = int((num_songs * 4) / 5) # divide data into train and test
             keys = songs.keys()

             train = keys[:slash]
             test = keys[slash:]

             tmpDict = {}
             for i in train:
                 tmpDict[i] = songs.get(i)
             train = tmpDict
             tmpDict = {}
             for i in test:
                 tmpDict[i] = songs.get(i)
             test = tmpDict
             
             testDict[user] = test
         trainDict[user] = train
     print len(trainDict)
     print "\n"     
     
     print len(testDict)
     print count
     print len(trackCountDict.keys())
     
     it = testDict.iteritems()
     for i in testDict:
          k,v = it.next()
          tmpDict = {}
          tmpDict[k] = v
          db.contentTest.insert_one(tmpDict)
          
     it = trainDict.iteritems()
     for i in trainDict:
          k,v = it.next()
          tmpDict = {}
          tmpDict[k] = v
          db.contentTrain.insert_one(tmpDict)

     print("--- %s seconds ---" % (time.time() - start_time))