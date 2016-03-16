"""
Created on 12 Aug 2014

@author: neil.butcher
"""

from models import Measurement as MeasurementObject, UnitMeasurementException
from ConglomerateWidgets import UnitEntryField, SingleMeasurementEntryFieldStack, MeasurementEntryGridField
from UnitComboDelegate import UnitComboDelegate

_measurements = {}


def Measurement(name):
    if name not in _measurements:
        _measurements[name] = MeasurementObject(name)
    return _measurements[name]


def Unit(measurement, name):
    for u in measurement.units:
        if u.name == name:
            return u
    raise UnitMeasurementException("There is no unit for " + str(measurement) + " by the name: " + name)
