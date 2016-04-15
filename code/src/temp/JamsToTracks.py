import csv
from pymongo import MongoClient
import os
import time

start_time = time.time()
client = MongoClient()
db = client.temp_database
jams = db.jams

#cursors = db.jams.find({'title':'Rip It Up','artist':'Orange Juice'})
cursors = db.jams.find()
counter = 0

for c in cursors:
	title = c['title'].strip()
	artist = c['artist'].strip()
	
	tcursors = db.tracks.find({'title':title,'artist_name':artist})
	
	if(tcursors.count() > 0):
		#print tcursors.count()
		counter = counter + 1
		
		'''
		for t in tcursors:
			print t['song_id']
			print t['track_id']
			print c['jam_id']
			print t['title']
			print t['artist_name']
			print t['artist_id']
			print '\n'
		
		print '\n\n'
		#break
		'''

print counter
print("--- %s seconds ---" % (time.time() - start_time))
