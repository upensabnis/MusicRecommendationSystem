# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 23:28:21 2016

@author: nachiketbhagwat
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 21:28:00 2016

@author: nachiketbhagwat
"""

import time

from HandleGenre import apriori
from HandleGenre import deleteGenre

start_time = time.time()
genres = apriori("127.0.0.1", 27017,"temp_database", "tracks", "artist_terms", 0.1)
'''print genres
print len(genres)
'''

deleteGenre("127.0.0.1", 27017,"temp_database", "tracks", "artist_terms", genres)
    
print("--- %s seconds ---" % (time.time() - start_time))