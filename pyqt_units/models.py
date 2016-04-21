'''
Created on 12 Aug 2014

@author: neil.butcher
'''

import sqlite3
from .MeasurementDatabase import filename
from .CurrentUnitSetter import setter

_connection = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)


class UnitMeasurementException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Measurement(object):
    def __init__(self, name=None):
        self.name = name
        self._unitsCache = None
        self._id_cache = None
        self._baseUnitCache = None

    def __str__(self):
        return self.name + "<Measurement>"

    @property
    def baseUnit(self):
        if self._unitsCache is None:
            self.units
        return self._baseUnitCache

    def _units(self):
        if self._unitsCache is None:
            self._unitsCache = {}
            cursor = _connection.execute("SELECT name , Scale , offset ,id , base FROM UNITS WHERE measurementID = ?",
                                         (self._id(),))
            for row in cursor:
                unit = Unit()
                unit.measurement = self
                unit.name = row[0]
                unit.scale = float(row[1])
                unit.offset = float(row[2])
                unit.id_cache = row[3]
                self._unitsCache[row[3]] = unit
                if row[4] == 1:
                    self._baseUnitCache = unit
            if self._baseUnitCache is None:
                raise UnitMeasurementException("There was no unit to act as the base unit for measurement " + self.name)
        return self._unitsCache

    @property
    def units(self):
        return self._units().values()

    def _id(self):
        if self._id_cache is None:
            cursor = _connection.execute("SELECT id  FROM MEASUREMENTS WHERE name = ?", (self.name,))
            for row in cursor:
                if self._id_cache is None:
                    self._id_cache = row[0]
                else:
                    raise UnitMeasurementException("There are multiple measurements with the same name")
            if self._id_cache is None:
                raise UnitMeasurementException("There was no measurements with this name in the database")
        return self._id_cache

    def currentUnit(self, label='normal'):
        cursor = _connection.execute("SELECT unitID  FROM CurrentUnits WHERE measurementID = ? AND label = ? ",
                                     (self._id(), label))
        for row in cursor:
            return self._units()[row[0]]
        return None

    def setCurrentUnit(self, u, label='normal'):
        _connection.execute("UPDATE CurrentUnits set unitID = ? where measurementID = ? AND label = ? ",
                            (u.id_cache, self._id_cache, label))
        _connection.commit()

    def report(self, base_value, decimalPlaces=3, label='normal', writeUnit=True):
        try:
            scaled_value = self.currentUnit(label).scaledValueOf(base_value)
            text = '%.*f' % (decimalPlaces, scaled_value)
        except (ValueError, TypeError):
            text = str(base_value)
        if writeUnit:
            text = text  + ' (' + self.currentUnit(label).name + ')'
        return text

    def scaledValueOf(self, base_float, label='normal'):
        return self.currentUnit(label).scaledValueOf(base_float)


class Unit(object):
    def __init__(self):
        self.name = None
        self.measurement = None
        self.scale = 1.0
        self.offset = 0.0
        self.id_cache = 0

    def __str__(self):
        return self.name + "<Unit>"

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
        return self.measurement.baseUnit

    def currentUnit(self, label='normal'):
        return self.measurement.currentUnit(label=label)

    def becomeCurrentNormalUnit(self):
        setter.setMeasurementUnit(self.measurement, self)
    
