import csv
from pymongo import MongoClient
import sys
import csv
import os
import time

csv.field_size_limit(sys.maxsize)

def loadTSVData():
	'''
	############## Load follower.tsv in mongodb ################
	print "Loading followers data ........"
	start_time = time.time()
	client = MongoClient()
	db = client.temp_database
	followers = db.followers
	counter = 0

	with open('followers.tsv', 'rb') as csvfile:
		followersreader = csv.reader(csvfile, delimiter='	', quotechar='|')
		
		for row in followersreader:
			if(counter == 0):
				counter = counter + 1
				continue
				
			#if(counter == 5):
			#	break	
			
			followersDict = {}
			followersDict['_id'] = "f"+ str(counter).zfill(10)
			followersDict['followed'] = row[0]
			followersDict['follower'] = row[1]
			db.followers.insert(followersDict)
			counter = counter + 1

	print "Loading followers data done"
	
	######## Load likes.tsv in mongodb ###############
	print "Loading likes data ........"
	client = MongoClient()
	db = client.temp_database
	likes = db.likes
	counter = 0

	with open('likes.tsv', 'rb') as csvfile:
		likesreader = csv.reader(csvfile, delimiter='	', quotechar='|')
		
		for row in likesreader:
			if(counter == 0):
				counter = counter + 1
				continue
					
			#if(counter == 5):
			#	break	
			
			likesDict = {}
			likesDict['_id'] = "l"+ str(counter).zfill(10)
			likesDict['user_id'] = row[0]
			likesDict['jam_id'] = row[1]
			db.likes.insert(likesDict)
			counter = counter + 1

	print "Loading likes dat done"
	
	######## Load jams.tsv in mongodb ###############
	print "Loading jams data ........"
	client = MongoClient()
	db = client.temp_database
	jams = db.jams
	counter = 0

	with open('jams.tsv', 'rU') as csvfile:
		jamsreader = csv.reader(csvfile, delimiter='	', quotechar='|')
		
		for row in jamsreader:
			if(counter == 0):
				counter = counter + 1
				continue
					
			#if(counter == 1000):
			#	break	
			
			if(len(row) == 7):
				jamsDict = {}
				jamsDict['_id'] = "j"+ str(counter).zfill(10)
				jamsDict['user_id'] = row[0]
				jamsDict['title'] = row[1]
				jamsDict['artist'] = row[2]
				jamsDict['jam_id'] = row[3]
				jamsDict['creation_date'] = row[4]
				jamsDict['link'] = row[5]
				jamsDict['spotify'] = row[6]
			
				db.jams.insert(jamsDict)
				counter = counter + 1
	
	######## Load tracks.csv from EC2 in mongodb ###############
	print "Loading tracks data ........"
	start_time = time.time()
	client = MongoClient()
	db = client.music_database
	tracks = db.tracks
	counter = 0

	with open('tracks.csv', 'rU') as csvfile:
		treader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		for row in treader:
			if(counter == 0):
				counter = counter + 1
				continue
					
			if(counter == 10):
				break	
			
			if(len(row) == 17):
				tracksDict = {}
				print row[0]
				print row[1]
				print row[2]
				print row[3]
				
				a_t = []
				for r in row[0]:
					a_t.append(r)
				tracksDict['artist_terms'] = a_t
				
				m_t = []
				for m in row[1]:
					m_t.append(m)
				tracksDict['artist_mbtags'] = a_t
				
				tracksDict['similar_artists'] = row[2]
				tracksDict['artist_familiarity'] = row[3]
				tracksDict['artist_hotttnesss'] = row[4]
				tracksDict['artist_id'] = row[5]
				tracksDict['artist_name'] = row[6]
				tracksDict['danceability'] = row[7]
				tracksDict['duration'] = row[8]
				tracksDict['energy'] = row[9]
				tracksDict['loudness'] = row[10]
				tracksDict['release'] = row[11]
				tracksDict['song_hotttnesss'] = row[12]
				tracksDict['song_id'] = row[13]
				tracksDict['tempo'] = row[14]
				tracksDict['title'] = row[15]
				tracksDict['track_id'] = row[16]
			
				db.tracks.insert(tracksDict)
				
				counter = counter + 1
	'''
	
	######## Load tracks.csv from EC2 in mongodb ###############
	print "Loading tracks data ........"
	start_time = time.time()
	client = MongoClient()
	db = client.temp_database
	tracks = db.tracks
	counter = 0

	with open('tracks.tsv', 'rU') as csvfile:
		treader = csv.reader(csvfile, delimiter='	', quotechar='|')
		
		for row in treader:
			if(counter == 0):
				counter = counter + 1
				continue
					
			#if(counter == 2):
			#	break	
			
			if(len(row) == 17):
				tracksDict = {}
				
				o_str = row[0]
				stripped = o_str[4:]
				stripped = stripped[:len(stripped)-4]
				a = stripped.split("\"\",\"\"")
				a_t = []	
				for r in a:
					a_t.append(r)
				tracksDict['artist_terms'] = a_t
				
				m_str = row[1]
				stripped = m_str[4:]
				stripped = stripped[:len(stripped)-4]
				a = stripped.split("\"\",\"\"")
				m_t = []	
				for r in a:
					m_t.append(r)
				
				tracksDict['artist_terms'] = m_t
				
				tracksDict['similar_artists'] = row[2]
				tracksDict['artist_familiarity'] = float(row[3])
				tracksDict['artist_hotttnesss'] = float(row[4])
				tracksDict['artist_id'] = row[5]
				tracksDict['artist_name'] = row[6]
				tracksDict['danceability'] = float(row[7])
				tracksDict['duration'] = float(row[8])
				tracksDict['energy'] = float(row[9])
				tracksDict['loudness'] = float(row[10])
				tracksDict['release'] = row[11]
				tracksDict['song_hotttnesss'] = float(row[12])
				tracksDict['song_id'] = row[13]
				tracksDict['tempo'] = float(row[14])
				tracksDict['title'] = row[15]
				tracksDict['track_id'] = row[16]
			
				db.tracks.insert(tracksDict)
				
				counter = counter + 1
							
	print("--- %s seconds ---" % (time.time() - start_time))
	print "Loading EC2 tracks data done"

loadTSVData()    