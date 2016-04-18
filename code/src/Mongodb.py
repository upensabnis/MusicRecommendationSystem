# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 19:03:59 2016

@author: nachiketbhagwat
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 17:18:14 2016

@author: nachiketbhagwat
"""

import os
import time
from ExtractFields import extractValues
from pymongo import MongoClient

BASE_DIR = "/home/user/Documents/datamining/project/MillionSongSubset/data/"

count = 0
start_time = time.time()
client = MongoClient()


db = client.temp_database
tracks = db.tracks


for (dir, _, files) in os.walk(BASE_DIR):
    for f in files:
        path = os.path.join(dir, f)
        fields = [
            "artist_terms",
            "artist_mbtags",
            "bars_confidence",
            "beats_confidence",
            "similar_artists",
            #"analysis_sample_rate", #problem
            "artist_familiarity",
            "artist_hotttnesss",
            "artist_id",
            "artist_name",
            #"year", #problem
            "danceability",
            "duration",
            "energy",
            "loudness",
            "release",
            "song_hotttnesss",
            "song_id",
            "tempo",
            #"time_signature", #problem
            "title",
            "track_id"
        ]
        output = extractValues(path, False, fields)
        #print type(output)
        #print output 
        tmp = {} 
        result = db.tracks.insert_one(output)
        print result
        
        
        count = count + 1
    
        
print count
print("--- %s seconds ---" % (time.time() - start_time))
