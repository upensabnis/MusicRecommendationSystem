import csv
from pymongo import MongoClient
import os
import time
import sys

#def calculateMissingValues():
print "Calculating missing values ...."
start_time = time.time()
client = MongoClient()
db = client.temp_database
tracks = db.tracks
cursors = db.tracks.find()
countsh = 0
sumsh = 0
countaf = 0
sumaf = 0
counttempo = 0
sumtempo = 0
countld = 0
sumld = 0
counten = 0
sumen = 0
countdr = 0
sumdr = 0
countda = 0
sumda = 0
countah = 0
sumah = 0
maxfloat = sys.float_info.max

################### Traverse over cursors to calculate sum of each column ####################
for c in cursors:
	if(c['song_hotttnesss'] != maxfloat):
		sumsh = sumsh + c['song_hotttnesss']
		countsh = countsh+1
	if(c['artist_familiarity'] != maxfloat):
		sumaf = sumaf + c['artist_familiarity']
		countaf = countaf+1
	if(c['tempo'] != maxfloat):
		sumtempo = sumtempo + c['tempo']
		counttempo = counttempo+1
	if(c['loudness'] != maxfloat):
		sumld = sumld + c['loudness']
		countld = countld+1
	if(c['energy'] != maxfloat):
		sumen = sumen + c['energy']
		counten = counten+1
	if(c['duration'] != maxfloat):
		sumdr = sumdr + c['duration']
		countdr = countdr+1
	if(c['danceability'] != maxfloat):
		sumda = sumda + c['danceability']
		countda = countda+1
	if(c['artist_hotttnesss'] != maxfloat):
		sumah = sumah + c['artist_hotttnesss']
		countah = countah+1

##################### Calculate golbal mean for each column ################################
if countsh > 0:
	avgsh = sumsh / countsh
else:
	avgsh = 0

if countaf > 0:
	avgaf = sumaf / countaf
else:
	avgaf = 0
		
if counttempo > 0:
	avgtempo = sumtempo / counttempo
else:
	avgtempo = 0
	
if countld > 0:
	avgld = sumld / countld
else:
	avgld = 0
		
if counten > 0:
	avgen = sumen / counten
else:
	avgen = 0
		
if countdr > 0:
	avgdr = sumdr / countdr
else:
	avgdr = 0
		
if countda > 0:
	avgda = sumda / countda
else:
	avgda = 0
		
if countah > 0:
	avgah = sumah / countah
else:
	avgah = 0

	#print avgsh
	#print avgaf
	#print avgtempo
	#print avgld
	#print avgen
	#print avgdr
	#print avgda
	#print avgah


###################### Replace the missing values with calculated global mean #################################
cursors = db.tracks.find()
for c in cursors:
	if (c['song_hotttnesss'] == maxfloat):
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"song_hotttnesss": avgsh}})
	if (c['artist_familiarity'] == maxfloat) :
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"artist_familiarity": avgaf}})
	if (c['tempo'] == maxfloat) :
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"tempo": avgtempo}})
	if (c['loudness'] == maxfloat) :
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"loudness": avgld}})
	if (c['energy'] == maxfloat) :
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"energy": avgen}})
	if (c['duration'] == maxfloat) :
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"duration": avgdr}})
	if (c['danceability'] == maxfloat) :
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"danceability": avgda}})
	if (c['artist_hotttnesss'] == maxfloat) :
		db.tracks.update_one( {"_id":c.get("_id")},{"$set": {"artist_hotttnesss": avgah}})
	
print("--- %s seconds ---" % (time.time() - start_time))		
print "Inserted missing values in mongo"
