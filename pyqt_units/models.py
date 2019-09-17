
#Created on 12 Aug 2014

#@author: neil.butcher


import sqlite3
from .MeasurementDatabase import filename
from .CurrentUnitSetter import setter
from PySide2 import QtCore




class UnitMeasurementException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Measurement(object):
    def __init__(self, name=None):
        self._name = name
        self._unitsCache = None
        self._id_cache = None
        self._baseUnitCache = None

    def __repr__(self):
        return "Measurement('" + self._name + "')"

    @property
    def baseUnit(self):
        """
        :rtype: Unit
        """
        if self._unitsCache is None:
            self._units()
        return self._baseUnitCache

    @property
    def name(self):
        """
        :rtype: str
        """
        _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = _connection.execute("SELECT name  FROM MEASUREMENTNAMES WHERE measurementID = ? AND preferred = 1 ",
                                     (self._id(),))
        for row in cursor:
            return row[0]

        _connection.execute("UPDATE MEASUREMENTNAMES set preferred = 1 where measurementID = ? AND name = ? ",
                                (self._id_cache, self._name))
        _connection.commit()
        return self._name


    def setPreferredName(self, name):
        """
        :type name: str
        """
        if name != self.name:
            _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
            _connection.execute("UPDATE MEASUREMENTNAMES set preferred = 0 where measurementID = ?",
                                (self._id_cache,))
            _connection.execute("UPDATE MEASUREMENTNAMES set preferred = 1 where measurementID = ? AND name = ? ",
                                (self._id_cache, name))
            _connection.commit()


    def addAlias(self, name):
        """
        :type name: str
        """
        if name != self.name:
            _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
            _connection.execute("INSERT INTO MEASUREMENTNAMES VALUES (?,?,?) ",
                                (self._id_cache, name, 0))
            _connection.commit()

    def _units(self):
        if self._unitsCache is None:
            self._unitsCache = {}
            _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = _connection.execute("SELECT name , Scale , offset ,id , base FROM UNITS WHERE measurementID = ?",
                                         (self._id(),))
            for row in cursor:
                unit = Unit()
                unit.measurement = self
                unit._name = row[0]
                unit.scale = float(row[1])
                unit.offset = float(row[2])
                unit.id_cache = row[3]
                self._unitsCache[row[3]] = unit
                if row[4] == 1:
                    self._baseUnitCache = unit
            if self._baseUnitCache is None:
                raise UnitMeasurementException("There was no unit to act as the base unit for measurement " + self._name)
        return self._unitsCache

    @property
    def units(self):
        return list(self._units().values())

    def _id(self):
        if self._id_cache is None:
            _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = _connection.execute("SELECT id  FROM MEASUREMENTS WHERE name = ?", (self._name,))
            for row in cursor:
                if self._id_cache is None:
                    self._id_cache = row[0]
                else:
                    raise UnitMeasurementException("There are multiple measurements with the same name")
            if self._id_cache is None:
                cursor = _connection.execute("SELECT measurementID  FROM MEASUREMENTNAMES WHERE name = ?", (self._name,))
                for row in cursor:
                    if self._id_cache is None:
                        self._id_cache = row[0]
                    else:
                        raise UnitMeasurementException("There are multiple measurements with the same name")
                if self._id_cache is None:
                    raise UnitMeasurementException("There was no measurements with this name in the database")
        return self._id_cache

    def currentUnit(self, label='normal'):
        """
        :type label: str
        :rtype: Unit
        """
        _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = _connection.execute("SELECT unitID  FROM CURRENTUNITS WHERE measurementID = ? AND label = ? ",
                                     (self._id(), label))
        for row in cursor:
            return self._units()[row[0]]

        self._units()
        _connection.execute("INSERT INTO CURRENTUNITS VALUES (?,?,?) ",
                            (self._id_cache, label, self.baseUnit.id_cache))
        _connection.commit()
        return self.baseUnit

    def setCurrentUnit(self, u, label='normal'):
        """
        :type u: Unit
        :type label: str
        """
        if u != self.currentUnit(label):
            _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
            _connection.execute("UPDATE CURRENTUNITS set unitID = ? where measurementID = ? AND label = ? ",
                                (u.id_cache, self._id_cache, label))
            _connection.commit()

    def report(self, base_value, precision=6, label='normal', writeUnit=True):
        try:
            scaled_value = self.currentUnit(label).scaledValueOf(base_value)
            text = QtCore.QLocale().toString(scaled_value, precision=precision)
        except (ValueError, TypeError):
            text = str(base_value)
        if writeUnit:
            text = text  + ' (' + self.currentUnit(label).name + ')'
        return text

    def scaledValueOf(self, base_float, label='normal'):
        return self.currentUnit(label).scaledValueOf(base_float)

    def baseValueFrom(self, base_float, label='normal'):
        return self.currentUnit(label).baseValueFrom(base_float)


class Unit(object):
    def __init__(self):
        self._name = None
        self.measurement = None
        self.scale = 1.0
        self.offset = 0.0
        self.id_cache = 0

    def __repr__(self):
        return "Unit(" +str(self.measurement) + ",'" + self.name + "')"

    def scaledValueOf(self, base_float):
        return (base_float / self.scale ) - self.offset

    def baseValueFrom(self, scaled_float):
        return (scaled_float + self.offset) * self.scale

    def scaledDeltaValueOf(self, base_float):
        # scale a change in the measurement (rather than an absolute value)
        #eg a change of 1Kelvin = a change of 1degC
        return (base_float / self.scale )

    def baseDeltaValueFrom(self, scaled_float):
        # scale a change in the measurement (rather than an absolute value)
        #eg a change of 1Kelvin = a change of 1degC
        return scaled_float * self.scale

    @property
    def baseUnit(self):
        """
        :rtype: Unit
        """
        return self.measurement.baseUnit

    def currentUnit(self, label='normal'):
        """
        :type label: str
        :rtype: Unit
        """
        return self.measurement.currentUnit(label=label)

    def becomeCurrentNormalUnit(self):
        setter.setMeasurementUnit(self.measurement, self)
    
    def alias(self):
        res = []
        _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = _connection.execute("SELECT name  FROM UNITNAMES WHERE unitID = ?",
                                     (self.id_cache,))
        for row in cursor:
            res.append(row[0])
        return res

    def addAlias(self, name):
        """
        :type name: str
        """
        if name != self.name:
            _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
            _connection.execute("INSERT INTO UNITNAMES VALUES (?,?,?) ",
                                (self.id_cache, name, 0))
            _connection.commit()

    @property
    def name(self):
        """
        :rtype: str
        """
        _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = _connection.execute("SELECT name  FROM UNITNAMES WHERE unitID = ? AND preferred = ? ",
                                     (self.id_cache, 1))
        for row in cursor:
            return row[0]

        _connection.execute("UPDATE UNITNAMES set preferred = ? where unitID = ? AND name = ? ",
                                (1, self.id_cache, self._name))
        _connection.commit()
        return self._name


    def setPreferredName(self, name):
        """
        :type name: str
        """
        if name != self.name:
            _connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
            _connection.execute("UPDATE UNITNAMES set preferred = ? where unitID = ?",
                                (0, self.id_cache,))
            _connection.execute("UPDATE UNITNAMES set preferred = ? where unitID = ? AND name = ? ",
                                (1, self.id_cache, name))
            _connection.commit()