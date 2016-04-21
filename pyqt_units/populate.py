'''
Created on 12 Aug 2014

@author: neil.butcher
'''

import sqlite3
from .MeasurementDatabase import filename
_connection = sqlite3.connect(filename, detect_types = sqlite3.PARSE_DECLTYPES)


def populateMeasurements(measurements):
    i = 0
    j = 0
    for a in measurements:
        print i
        _connection.execute('INSERT INTO MEASUREMENTS VALUES (?,?)', (i,a.name))
        _connection.execute('INSERT INTO CurrentUnits VALUES (?,?,?,?)', (3*i,i,'normal',j))
        _connection.execute('INSERT INTO CurrentUnits VALUES (?,?,?,?)', (3*i +1,i,'large',j))
        _connection.execute('INSERT INTO CurrentUnits VALUES (?,?,?,?)', (3*i+2,i,'small',j))
        for u in a.units.all() :
            _connection.execute('INSERT INTO UNITS VALUES (?,?,?,?,?,?)', (j, u.name,i, str(u.scale), str(u.offset), 0))
            j = j+1
        i = i+1
    _connection.commit()
    _connection.close()
    
        
    