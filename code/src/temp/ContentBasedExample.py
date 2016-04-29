# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 19:35:51 2016

@author: nachiketbhagwat
"""
import random
import time

songs_attr = 3

def DotProduct(v1, v2):
    ret = 0
    for i in range (0, songs_attr):
        ret = ret + v1[i]*v2[i]
    
    return ret

def GetThetas(songs, users, songsinfo, usersongs):
    
    thetas = []
    
    alpha = 0.0001
    lambdaa = 1000
    
    for j in range (0, users):
        thetas.append([1, 1, 1])
    for iterations in range(0,500):
        #print iterations
        for j in range(0, users):
            songlist = usersongs[j]
            keys = songlist.keys()
            #print type(keys)
            lens = len(keys)
            for i in range (0,lens):
                
                for k in range (0, songs_attr):
                    if k == 0:
                        thetas[j][k] = thetas[j][k] - alpha * (DotProduct(thetas[j], songsinfo[keys[i]])- songlist.get(keys[i])) * songsinfo[keys[i]][k]
                    
                    else:
                        thetas[j][k] = thetas[j][k] - alpha * ((DotProduct(thetas[j], songsinfo[keys[i]])- songlist.get(keys[i])) * songsinfo[keys[i]][k] +  lambdaa*thetas[j][k] )
    
    #for j in range(0, users):
    #    print thetas[j]
                
    
    
    return thetas

def CreateInfo(songs, users, songsinfo, usersongs):
    
    for i in range (0,songs):
        songsinfo.append([])
        for j in range (0, songs_attr):
            songsinfo[i].append(random.randint(1,10))
       
    for i in range (0,users):
        usersongs.append({})
        for j in range (0,10):
            usersongs[i][random.randint(1,songs)] = random.randint(1,5)

    
if __name__ == "__main__":
    users = 1000
    songs = 1000000
    songsinfo = []
    usersongs = []     
    CreateInfo(songs, users, songsinfo, usersongs)
    
    thetas = GetThetas(songs, users, songsinfo, usersongs)
    start_time = time.time()    
    for i in range (0,songs):
        #print DotProduct(thetas[0], songsinfo[i])
        DotProduct(thetas[0], songsinfo[i])
    print("--- %s seconds ---" % (time.time() - start_time))