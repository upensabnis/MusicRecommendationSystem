import csv
from pymongo import MongoClient

insertfollowersArray = []
with open('followers.tsv', 'rb') as csvfile:
	followersreader = csv.reader(csvfile, delimiter='	', quotechar='|')
	counter = 0
	for row in followersreader:
		if(counter == 0):
			counter = counter + 1
			continue
			
		if(counter == 5):
			break	
		print ', '.join(row)
		followersDict = {}
		followersDict['followed'] = row[0]
		followersDict['follower'] = row[1]
		insertfollowersArray.append(followersDict)
		counter = counter + 1
		
print insertfollowersArray

count = 0
client = MongoClient()

db = client.temp_database
followers = db.followers
result = db.followers.insert(insertfollowersArray)


print '\n\n'
client = MongoClient()
insertArray = []
with open('likes.tsv', 'rb') as csvfile:
	likesreader = csv.reader(csvfile, delimiter='	', quotechar='|')
	counter = 0
	for row in likesreader:
		if(counter == 0):
			counter = counter + 1
			continue
		
		likesDict = {}
		if(counter == 5):
			break	
		print ', '.join(row)
		likesDict['jam_id'] = row[0]
		likesDict['user_id'] = row[1]
		insertArray.append(likesDict)
		counter = counter + 1
		
print insertArray

db = client.temp_database
likes = db.likes
result = db.likes.insert(insertArray)
