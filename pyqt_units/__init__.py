
#Created on 17 Aug 2014

#@author: neil.butcher


from .models import Measurement as MeasurementObject, UnitMeasurementException
from .ConglomerateWidgets import UnitEntryField, SingleMeasurementEntryFieldStack, MeasurementEntryGridField
from .MeasurementWidgets import UnitDisplay, UnitComboBox, UnitSpinBox
from .UnitComboDelegate import UnitComboDelegate
from .CurrentUnitSetter import setter as _setter
from . import SelectionMenu

_measurements = {}

def menu(parent):
    #only those measurements which have been used for something
    return SelectionMenu.menu(_measurements.values(),parent)

def Measurement(name):
    if name not in _measurements:
        _measurements[name] = MeasurementObject(name)
    return _measurements[name]


def Unit(measurement, name):
    for u in measurement.units:
        if u.name == name:
            return u
    for u in measurement.units:
        if name in u.alias:
            return u
    raise UnitMeasurementException("There is no unit for " + str(measurement) + " by the name: " + name)

def changedSignal():
    return _setter.changed