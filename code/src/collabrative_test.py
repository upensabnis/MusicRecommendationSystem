import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

import time
import random
import numpy
import itertools
import operator
from HandleGenre import apriori
from HandleGenre import deleteGenre

client = MongoClient()

db = client.temp_database
track = db.tracks

db2=client.jam_database
jam = db2.jams
cluster=db2.cluster
user_gener=db2.user_gener

cluster_centroid = {}
user_centroid={}
user_data_random={}

for clusters in cluster.find():
	cluster_centroid[clusters['cluster']]=clusters['cluster_centroid']

user_data={}
for collection in user_gener.find():
	user_data[collection.get('user_id')]=collection.get('track')

for i in range(10):
	values=[]
	userId=random.choice(user_data.keys())
	user_data_random[userId]=user_data[userId]

#print user_data_random
	
user_loop=list(user_data_random.keys())   #gets all the usersId's

temp={}

for user in user_loop:   #Changes the dic in the format userId:[values of tracks]
	values=[]
	temp=user_data.get(user)
	values=list(temp.values())
	user_data_random[user]=values
	
#print cluster_centroid

artist_title_data={}

for collection in jam.find():
	artist_title_data[collection['title']]=[]

for collection in jam.find():
	newvalue=[]
	newvalue.append(collection.get('artist'))
	newvalue.append(collection.get('jam_id'))
	#print newvalue
	artist_title_data[collection['title']].append(newvalue)
	
print "Jam data is loaded"

track_artists = {}
for collection in track.find({},no_cursor_timeout=True):
	newKey = collection['artist_name'].join(':').join(collection['title'])
	track_artists[newKey] = collection['title']

print "track data loaded"
	
def calc_correlation(centroid,userterm):  
	N=len(centroid)
	XMean=numpy.mean(centroid)
	YMean=numpy.mean(userterm)
	Xstd=numpy.std(centroid)
	Ystd=numpy.std(userterm)
	denominator=N*Xstd*Ystd
	correlation=0
	for x,y in zip(centroid,userterm):
		correlation=correlation+(x*y-XMean*YMean)
	try:
		correlation=correlation/denominator
	except ZeroDivisionError:
		print "Denominator zero"
	return correlation

def get_user_songs(user):
	user_songs_list={}
	counter=1
	artist_songs=[]
	artist_songs=artist_title_data[user]
	
	for data in artist_songs:
		user_songs_list[counter]=data[1]
		counter=counter+1
	
	'''
	for collection in jam.find({'title':user}):
		user_songs_list[counter]=collection['jam_id']
		counter=counter+1'''
		
	return user_songs_list


def gettopsongs(cluster_selection):
	cluster_data={}
	cluster_users=[]
	user_songs={}
	
	for data in cluster.find():
		cluster_data[data['cluster']]=data['users']

	cluster_users=cluster_data[cluster_selection]
	#cluster_users=cluster_data[cluster_selection]
	
	#print "got cluster data"	
	#print cluster_users
	usertosongs={}
	#print "Inside get top songs"
	
	artist_data=[]
	titles=[]
	artists=[]
	
	for user in cluster_users:
		artists=artist_title_data[user]
		for value in artists:
			artist_data.append(value[0])
			titles.append(value[1])

	'''for user in cluster_users:			#This will get all the songs listen by each user in the cluster
		for data in jam.find({'title':user}):
			titles.append(data['jam_id'])
			artists.append(data['artist'])'''
	
	'''for collection in jam.find():
		if jam['title']==user:
			titles.append(data['jam_id'])
			artist.append(data['artist'])'''

	#print "Got the songs from the jams"
	print len(titles),len(artist_data)

	
	songs_count={}

	for title in titles:
		songs_count[title]=0

	
	
	for t,a in zip(titles,artist_data): #This will get the matching song from the tracks tables
		#for data in track.find({'title':title,'artist_name':artist}):
		searchKey = a.join(':').join(t)
		if track_artists.get(searchKey ):	
			songs_count[t]=songs_count[t]+1
	'''
	songs_count={}

	for title in titles:
		songs_count[title]=0

	for title,artist in zip(titles,artist): #This will get the matching song from the tracks tables
		for data in track.find({'title':title,'artist_name':artist}):
			print "Match"
			songs_count[title]=songs_count[title]+1'''
	

	final_songs={}
	for key,value in songs_count.items(): #This will elimiate the songs with zero song count
		if value!=0:
			final_songs[key]=value
	
	
	return final_songs

def getaccuracy(user_songs,top_songs):
	count=0
	for user_song in user_songs:
		if user_song in top_songs:
			#print "Hit"
			count=count+1
	return count

def cluster_calcuation():
	start_time=time.time()
	centroid_id=[]
	clusters={}
	centroid_id=list(cluster_centroid.keys())
	count=1
	for users in centroid_id:
		clusters[users]=[]
	for user in user_loop:
		print "user",count
		user_centroid_belongs=0
		user_value=[]
		user_value=user_data_random[user]
		correlation_values=[]
		max_value=0
		top_songs={}
		user_songs={}
		for centroid_user in centroid_id:
			centroid_value= cluster_centroid[centroid_user]
			correlation_values.append(calc_correlation(centroid_value,user_value))
		max_value=max(correlation_values)
		clusters[centroid_id[correlation_values.index(max_value)]].append(user)
		user_centroid_belongs=centroid_id[correlation_values.index(max_value)]
		
		'''for centroid_user in centroid_id:
			if len(clusters[centroid_user])==1:
				user_centroid_belongs=centroid_user
				print "centroid",user_centroid_belongs'''
		
		user_songs=get_user_songs(user)
	
		#print user_songs
		print "centroid",user_centroid_belongs
		
		top_songs=gettopsongs(user_centroid_belongs)
	
		#print top_songs
		percentage=0
		hits=0
		hits=getaccuracy(list(user_songs.values()),list(top_songs.keys()))
		#print len(top_songs.keys())
		if len(top_songs.keys())!=0:
			percentage=((float(hits)/len(top_songs.keys()))*100)
			print "Total hits are",hits
			print "Percentage",percentage
		else:
			print "No Top songs"
		count=count+1
	print("--- %s seconds ---" % (time.time() - start_time))	
	
def main():
	cluster_calcuation()
	
main()
