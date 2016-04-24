# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:02:40 2016

@author: nachiketbhagwat
"""
import os
import time
from pymongo import MongoClient

songs_attr = 7
songDict = {}
userDict = {}

def DotProduct(v1, v2):
    ret = 0
    for i in range (0, songs_attr):
        ret = ret + v1[i]*v2[i]
    
    return ret

def GetThetas(songs, users, songsinfo, usersongs, thetas):
    alpha = 0.0001
    lambdaa = 0
    thetas = []
    
    for j in range (0, users):
        thetas.append([1, 1, 1,1,1,1,1])#iniialize thetas to zero
    
        
    for iterations in range(0,20):
        print iterations
        usersKeys = usersongs.keys()
        for j in range(0, users):#for j users
            uId = usersKeys[j]
            songlist = usersongs.get(uId)
            songKeys = songlist.keys()
            length = len(songKeys)
            for i in range (0,length):#for i songs
                for k in range (0, songs_attr):#for k attributes
                    songId = songKeys[i]
                    if k == 0:
                        
                        thetas[j][k] = thetas[j][k] - alpha * (DotProduct(thetas[j], songsinfo[songId])- songlist.get(songId)) * songsinfo[songId][k]
                    
                    else:
                        thetas[j][k] = thetas[j][k] - alpha * ((DotProduct(thetas[j], songsinfo[songId])- songlist.get(songId)) * songsinfo[songId][k] +  lambdaa*thetas[j][k] )
    #print thetas[0]
    return thetas

def initSong(songDict):
    client = MongoClient()
    db = client.temp_database
    tracks = db.tracks
    
    cursor = tracks.find()
    for track in cursor:
        try:
           song_id = track.get('song_id')
           values = []
           values.append(track.get("artist_familiarity"))
           values.append(track.get("artist_hotttnesss"))
           values.append(track.get("danceability"))
           values.append(track.get("energy"))
           values.append(track.get("loudness"))
           values.append(track.get("song_hotttnesss"))
           values.append(track.get("tempo"))
           if(songDict.has_key(song_id) == False):
               songDict[song_id] = values
           
        except:
           continue
    client.close()
    return
    
def initUser(userDict):
    client = MongoClient()
    db = client.temp_database
    contentTrain = db.contentTrain
    cursor = contentTrain.find()
    for user in cursor:
        try:
            keys = user.keys()
            for j in keys:
                if(str(j) != "_id"):
                    uId = str(j)
                    songs = user[uId]
                    userDict[uId] = songs
            
        except:
            continue
        
def initUserTest(userDictTest):
    client = MongoClient()
    db = client.temp_database
    contentTest = db.contentTest
    cursor = contentTest.find()
    for user in cursor:
        try:
            keys = user.keys()
            for j in keys:
                if(str(j) != "_id"):
                    uId = str(j)
                    songs = user[uId]
                    userDictTest[uId] = songs
            
        except:
            continue

start_time = time.time()
initSong(songDict)
initUser(userDict)
thetas = []
thetas = GetThetas(len(songDict), len(userDict), songDict, userDict, thetas)
userDictTest = {}
initUserTest(userDictTest)

final = 0
length = len(userDictTest)
sum0 = 0
sum1 = 0
for i in range(0, length):
    count0 = 0
    count1 = 0
    user = userDictTest.keys()[i]
    usongs = userDictTest[user]
    index = userDict.keys().index(user)
    #print index
    for j in usongs.keys():
        v1 = songDict.get(j)
        v2 = thetas[index]
        product = DotProduct(v1,v2)
        if(product)> 1:
            count0 = count0 + 1
        if(product)> 0.75:
            count1 = count1 + 1
    sum0 = sum0 + float(count0)/len(usongs)
    sum1 = sum1 + float(count1)/len(usongs)
print sum0/length
print sum1/length
print("--- %s seconds ---" % (time.time() - start_time))
