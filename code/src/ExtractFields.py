# -*- coding: utf-8 -*-

"""
Thierry Bertin-Mahieux (2010) Columbia University
tb2332@columbia.edu

Code to quickly see the content of an HDF5 file.

This is part of the Million Song Dataset project from
LabROSA (Columbia University) and The Echo Nest.


Copyright 2010, Thierry Bertin-Mahieux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import hdf5_getters
import numpy as np

def extractValues(hdf5path, summary, fields):

#    summary = False
    
    songidx = 0
    onegetter = ''
    h5 = hdf5_getters.open_h5_file_read(hdf5path)

    # get all getters
    keys = filter(lambda x: x[:4] == 'get_', hdf5_getters.__dict__.keys())
    getters = []
    
    keys.remove("get_num_songs") # special case
    for onegetter in fields:
        if onegetter[:4] != 'get_':
            onegetter = 'get_' + onegetter #add get_
            try:
                keys.index(onegetter) #find if keyval exists else exit
            except ValueError:
                print 'ERROR: getter requested:',onegetter,'does not exist.'
                h5.close()
                sys.exit(0)
            getters.append(onegetter)
    
    getters = np.sort(getters)
    
    retDict = {}

    # print them
    for getter in getters:
        try:
            res = hdf5_getters.__getattribute__(getter)(h5,songidx)
        except AttributeError, e:
            if summary:
                continue
            else:
                print e
                print 'forgot -summary flag? specified wrong getter?'
        if res.__class__.__name__ == 'ndarray':
            #print getter[4:]+": shape =",res.shape
            newlist = []            
            for i in res:
                newlist.append(i)
            #print newlist 
            
            retDict[getter[4:]] = newlist
            
        else:
            retDict[getter[4:]] = res
            print getter[4:]+":",res

    # done
    #print 'DONE, showed song',songidx,'/',numSongs-1,'in file:',hdf5path
    h5.close()
    print retDict
    return retDict    
