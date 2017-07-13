
#Created on 12 Aug 2014

#@author: neil.butcher


import sqlite3
from pyqt_units.MeasurementDatabase import filename
from pyqt_units import *

if __name__ == '__main__':
    _connection = sqlite3.connect(filename+'_new', detect_types=sqlite3.PARSE_DECLTYPES)
    
    _c = _connection.cursor()
    try:
        _c.execute('''DROP TABLE MEASUREMENTS''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE MEASUREMENTS
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

    try:
        _c.execute('''DROP TABLE MEASUREMENTNAMES''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE MEASUREMENTNAMES
        ( measurementID INTEGER, name TEXT UNIQUE, preferred INTEGER)''')

    try:
        _c.execute('''DROP TABLE UNITS''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE UNITS
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, measurementID INTEGER, Scale TEXT, offset TEXT, base INTEGER)''')

    try:
        _c.execute('''DROP TABLE UNITNAMES''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE UNITNAMES
        ( unitID INTEGER, name TEXT UNIQUE, preferred INTEGER)''')

    try:
        _c.execute('''DROP TABLE UNITHIDE''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE UNITHIDE
        ( unitID INTEGER, hide INTEGER)''')

    try:
        _c.execute('''DROP TABLE CURRENTUNITS''')
    except sqlite3.OperationalError:
        pass
    _c.execute('''CREATE TABLE CURRENTUNITS
             (measurementID INTEGER, label TEXT, unitID INTEGER)''')

    j = 1
    for i, n in enumerate(measurements_list()):

        m = Measurement(n)
        _c.execute("INSERT INTO MEASUREMENTS (name) VALUES (?) ",(n,))
        _c.execute("INSERT INTO MEASUREMENTNAMES VALUES (?, ?, ?) ",(i+1,n,1))
        for u in m.units:
            _c.execute('INSERT INTO UNITS (name,  measurementID,  Scale,  offset,  base) VALUES (?,?,?,?,?)',
                                (u.name, i+1, str(u.scale), str(u.offset), m.baseUnit == u))
            _c.execute("INSERT INTO UNITNAMES VALUES (?, ?, ?) ",(j,u.name,1))
            for a in u.alias():
                try:
                    _c.execute("INSERT INTO UNITNAMES VALUES (?, ?, ?) ",(j,a,0))
                except sqlite3.IntegrityError:
                    pass
            j=j+1
        print(m)


    _c.close()
    _connection.commit()
    _connection.close()