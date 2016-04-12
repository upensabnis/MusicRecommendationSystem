# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 23:30:44 2016

@author: nachiketbhagwat
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 20:15:14 2016

@author: nachiketbhagwat
"""

from pymongo import MongoClient

def apriori(ip, port, dbName, collectionName, term, support):    
    count = 0
    client = MongoClient(ip, port)
    db = client[dbName]
    collection = db[collectionName]
    at = collection.find({})
    genres = {}
    
    for doc in at:
        if(doc.has_key(term)): #& type(doc.get(term) == list)):
            try:
                artist_terms = doc.get(term)
                for genre in artist_terms:
                    if(genres.has_key(genre)):
                        genres[genre] = genres[genre] + 1
                    else:
                        genres[genre] = 1
                
                count = count + 1
            except AttributeError, e:
                print e
                print 'forgot -summary flag? specified wrong getter?'

    frequency = count * (support)
    
    keys = genres.keys()
    for genre in keys:
        if(genres.get(genre) < frequency):
            del genres[genre]
        
    return genres.keys()
    client.close()
    
'''
def PushGenres(ip, port, dbName, collectionName, doc):
    client = MongoClient(ip, port)
    db = client[dbName]
    collection = db[collectionName]
    collection.drop()
    result = db.collection.insert_one(doc)
    client.close()
    return
'''
    
def deleteGenre(ip, port, dbName, collectionName, term, values):
    client = MongoClient(ip, port)
    db = client[dbName]
    collection = db[collectionName]    
    at = collection.find({})
    for doc in at:
        if(doc.has_key(term)): #& type(doc.get(term) == list)):
            termValues = doc.get(term)
            for i in termValues:
                flag = 0
                for j in values:
                    if i == j:
                        flag = 1
                        break
                if flag == 0:
                    termValues.remove(i)
            #print termValues
            try:
                result = collection.update_one( {"_id": doc.get("_id")},
                                                 {"$set": {term: termValues}}
                                            )
                #break
            except AttributeError, e:
                print e
                print 'forgot -summary flag? specified wrong getter?'