import csv
from pymongo import MongoClient
import sys
import csv

csv.field_size_limit(sys.maxsize)

############## Load follower.tsv in mongodb ################

client = MongoClient()
db = client.temp_database
followers = db.followers
counter = 0

with open('/home/user/Documents/datamining/project/archive/followers.tsv', 'rb') as csvfile:
	followersreader = csv.reader(csvfile, delimiter='	', quotechar='|')
	
	for row in followersreader:
		if(counter == 0):
			counter = counter + 1
			continue
<<<<<<< HEAD
			
			
=======
>>>>>>> ef23933c2e3ec167ddfe0cad733453bee02451da
		
		followersDict = {}
		followersDict['_id'] = "f"+ str(counter).zfill(10)
		followersDict['followed'] = row[0]
		followersDict['follower'] = row[1]
		db.followers.insert(followersDict)
		counter = counter + 1


######## Load likes.tsv in mongodb ###############

client = MongoClient()
db = client.temp_database
likes = db.likes
counter = 0

with open('/home/user/Documents/datamining/project/archive/likes.tsv', 'rb') as csvfile:
	likesreader = csv.reader(csvfile, delimiter='	', quotechar='|')
	
	for row in likesreader:
		if(counter == 0):
			counter = counter + 1
			continue
<<<<<<< HEAD
				
=======
>>>>>>> ef23933c2e3ec167ddfe0cad733453bee02451da
		
		likesDict = {}
		likesDict['_id'] = "l"+ str(counter).zfill(10)
		likesDict['user_id'] = row[0]
		likesDict['jam_id'] = row[1]
		db.likes.insert(likesDict)
		counter = counter + 1


######## Load jams.tsv in mongodb ###############

client = MongoClient()
db = client.temp_database
jams = db.jams
counter = 0

with open('/home/user/Documents/datamining/project/archive/jams.tsv', 'rU') as csvfile:
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
