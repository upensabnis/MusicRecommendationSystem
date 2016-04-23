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

clusters={}

for c in cluster.find():
	clusters[c['cluster']]=c['users']
	
	
user_data={}

for collection in user_gener.find():
	user_data[collection.get('user_id')]=collection.get('track')

user_loop=list(user_data.keys())

for user in user_loop:   #Changes the dic in the format userId:[values of tracks]
	values=[]
	temp=user_data.get(user)
	values=list(temp.values())
	user_data[user]=values
	
#print user_data
	
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

	
def Intracluster_similarity():
	cluster_users=[]
	cluster_users=clusters[2]
	keys=[]
	keys=list(user_data.keys())
	userId=random.choice(user_data.keys())
	correlation_value=0
	correlation_value=calc_correlation(user_data.get(random.choice(cluster_users)),user_data.get(random.choice(cluster_users)))
	print "Intracluster_similarity",correlation_value
	
	
	
	
def Intercluster_similarity():
	cluster_users=[]
	cluster_users1=clusters[2]
	cluster_users2=clusters[1]
	keys=[]
	keys=list(user_data.keys())
	userId=random.choice(user_data.keys())
	correlation_value=0
	correlation_value=calc_correlation(user_data.get(random.choice(cluster_users1)),user_data.get(random.choice(cluster_users2)))
	print "Intercluster_similarity",correlation_value
	

def main():
	Intracluster_similarity()
	Intercluster_similarity()
	
main()
	




