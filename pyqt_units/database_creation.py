
#Created on 12 Aug 2014

#@author: neil.butcher


import sqlite3
from .MeasurementDatabase import filename

if __name__ == '__main__':
    _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
    
    _c = _connection.cursor()
    try:
        _c.execute('''DROP TABLE MEASUREMENTS''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE MEASUREMENTS
        (id INTEGER PRIMARY KEY, name TEXT)''')
    
    try:
        _c.execute('''DROP TABLE UNITS''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE UNITS
             (id INTEGER PRIMARY KEY, name TEXT, measurementID INTEGER, Scale TEXT, offset TEXT, base INTEGER)''')
    
    try:
        _c.execute('''DROP TABLE CurrentUnits''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE CurrentUnits
             (id INTEGER PRIMARY KEY, measurementID INTEGER, label TEXT, unitID INTEGER)''')