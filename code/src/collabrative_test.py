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
jam = db.jams
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

user_id=0
user_id=random.choice(user_data.keys())
user_data_random[user_id]=user_data[user_id]
print user_data_random
	
user_loop=list(user_data_random.keys())   #gets all the usersId's

temp={}

for user in user_loop:   #Changes the dic in the format userId:[values of tracks]
	values=[]
	temp=user_data.get(user)
	values=list(temp.values())
	user_data_random[user]=values
	
#print cluster_centroid
	
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
	for collection in jam.find({'title':user}):
		user_songs_list[counter]=collection['jam_id']
		counter=counter+1
	return user_songs_list


def gettopsongs(cluster_selection):
	cluster_data={}
	cluster_users=[]
	user_songs={}
	
	for data in cluster.find():
		cluster_data[data['cluster']]=data['users']

	cluster_users=cluster_data[cluster_selection]
	
	titles=[]
	artist=[]
	usertosongs={}
	print "Inside get top songs"
	
	for user in cluster_users:			#This will get all the songs listen by each user in the cluster
		for data in jam.find({'title':user}):
			titles.append(data['jam_id'])
			artist.append(data['artist'])
	
	'''for collection in jam.find():
		if jam['title']==user:
			titles.append(data['jam_id'])
			artist.append(data['artist'])'''

	print "Got the songs from the jams"
	print len(titles),len(artist)

	
	songs_count={}

	for title in titles:
		songs_count[title]=0

	track_artists = {}
	for collection in track.find({},no_cursor_timeout=True):
		newKey = collection['artist_name'].join(':').join(collection['title'])
		track_artists[newKey] = collection['title']
	
	for title,artist in zip(titles,artist): #This will get the matching song from the tracks tables
		#for data in track.find({'title':title,'artist_name':artist}):
		searchKey = artist.join(':').join(title)
		if track_artists.get(searchKey ):	
			songs_count[title]=songs_count[title]+1
	'''
	songs_count={}

	for title in titles:
		songs_count[title]=0

	for title,artist in zip(titles,artist): #This will get the matching song from the tracks tables
		for data in track.find({'title':title,'artist_name':artist}):
			print "Match"
			songs_count[title]=songs_count[title]+1'''
	

	final_songs={}
	for key,value in songs_count.items():
		if value!=0:
			final_songs[key]=value
			
	return final_songs

def getaccuracy(user_songs,top_songs):
	count=0
	for user_song in user_songs:
		if user_song in top_songs:
			print "Hit"
			count=count+1
	return count

def cluster_calcuation():
	centroid_id=[]
	clusters={}
	centroid_id=list(cluster_centroid.keys())
	for users in centroid_id:
			clusters[users]=[]
	for user in user_loop:
			user_value=[]
			user_value=user_data_random[user]
			correlation_values=[]
			max_value=0
			for centroid_user in centroid_id:
				centroid_value= cluster_centroid[centroid_user]
				correlation_values.append(calc_correlation(centroid_value,user_value))
			max_value=max(correlation_values)
			clusters[centroid_id[correlation_values.index(max_value)]].append(user)
			
	user_centroid_belongs=0
	top_songs={}
	for centroid_user in centroid_id:
		if len(clusters[centroid_user])==1:
			user_centroid_belongs=centroid_user
			print "centroid",user_centroid_belongs
	for user in user_loop:
		user_songs=get_user_songs(user)
	
	print user_songs
	top_songs=gettopsongs(user_centroid_belongs)
	
	print top_songs
	percentage=0
	hits=0
	hits=getaccuracy(list(user_songs.values()),list(top_songs.keys()))
	print len(top_songs.keys())
	percentage=((float(hits)/len(top_songs.keys()))*100)
	print percentage
	
def main():
	cluster_calcuation()
	
main()
