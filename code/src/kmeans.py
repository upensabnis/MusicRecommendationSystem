import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

import time
import random
import numpy
import itertools
from HandleGenre import apriori
from HandleGenre import deleteGenre


client = MongoClient()

db = client.jam_database
track = db.tracks
jam = db.jams
user_gener=db.user_gener

cluster={}
user_data={}
centroid={}
user_loop=[]


for collection in user_gener.find():
	user_data[collection.get('user_id')]=collection.get('track')
	
user_loop=list(user_data.keys())   #gets all the usersId's

temp={}

for user in user_loop:   #Changes the dic in the format userId:[values of tracks]
	values=[]
	temp=user_data.get(user)
	values=list(temp.values())
	user_data[user]=values
	
	
def getRandomCentroids(num_centroids): 	#return some random centroids
	temp={}
	for i in range(num_centroids):
		values=[]
		userId=random.choice(user_data.keys())
		centroid[i]=user_data[userId]
	return centroid
	
def getcentroids(clusters,length_tracks): #calculate the centroids mean and then get the new centroid points
	key=list(clusters.keys())
	value=list(clusters.values())
	
	count=0
	for users in value:
		count=count+1
		points=[]
		mean_value=[]
		for userid in users:
			points.append(user_data.get(userid))
		mean_value = mean(points,length_tracks)
		cluster[count]=mean_value
	return cluster
	
	
def mean(centroid,length_tracks):
	sum_centroid=[]
	for i in range(length_tracks):
		sum_centroid.append(0.0)
	
	for values in centroid:
		try:
			sum_centroid=[float(i+j) for i,j in zip(sum_centroid,values)]
		except:
			print "Type None"
	try:
		sum_centroid = [i/len(centroid) for i in sum_centroid]
	except ZeroDivisionError:
		print "Denominator Zero"
	return sum_centroid
	
	
	#Function to calculate correlatoin
	
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

		#function to check if centroids are same

def shouldstop(oldcentroids,centroids):
	print "" 
	key=list(centroids.keys())
	oldcentroid_value=[]
	centroid_value=[]
	oldcentroid_value=list(oldcentroids.values())
	centroid_value=list(centroids.values())
	if len(oldcentroid_value)!=0:
		for i in range(len(key)):
			if oldcentroid_value[i] != centroid_value[i]:
				return False
		return True
	return False
	
	### Main K-means clustering
	
def clustering():
	
	oldcentroids={}
	centroids=getRandomCentroids(10)    # centroids and old centroids are Dictonary
	start_time = time.time()
	while not shouldstop(oldcentroids,centroids):
		centroid_id=[]
		clusters={}
		centroid_id=list(centroids.keys())
		
		for users in centroid_id:
			clusters[users]=[]

		print "Kmeans"
		oldcentroids=centroids
		for user in user_loop:
			user_value=[]
			user_value=user_data[user]
			correlation_values=[]
			max_value=0
			for centroid_user in centroid_id:
				centroid_value= centroids[centroid_user]
				correlation_values.append(calc_correlation(centroid_value,user_value))
			max_value=max(correlation_values)
			clusters[centroid_id[correlation_values.index(max_value)]].append(user)
		
		for centroid_user in centroid_id:
			print centroid_user, len(clusters[centroid_user])
		
		#print clusters	
		centroids = getcentroids(clusters,len(centroid_value))	
	
	for key,value in clusters.items():
		mongo_data={}
		mongo_data['cluster']=key
		mongo_data['users']=value
		result = db.cluster.insert_one(mongo_data)
		print result
		
	print("--- %s seconds ---" % (time.time() - start_time))
		
		
		
		
			
		
def main():
	clustering()
	
main()
