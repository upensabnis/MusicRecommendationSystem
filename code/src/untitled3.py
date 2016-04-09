# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 21:28:00 2016

@author: nachiketbhagwat
"""

import time

from HandleGenre import Apriori
from HandleGenre import DeleteGenre
from HandleGenre import PushGenres

start_time = time.time()
genres = Apriori("127.0.0.1", 27017,"temp_database", "tracks", "artist_terms", 0.1)
print genres
print len(genres)

res = PushGenres("127.0.0.1", 27017,"temp_database", "genres", {"genres":genres})

#DeleteGenre("127.0.0.1", 27017,"temp_database", "tracks", "artist_terms", genres):
    
print("--- %s seconds ---" % (time.time() - start_time))