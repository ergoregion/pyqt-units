
#Created on 17 Aug 2014

#@author: neil.butcher


from .models import Measurement as MeasurementObject, UnitMeasurementException
from .models import Unit as UnitObject
from .ConglomerateWidgets import UnitEntryField, SingleMeasurementEntryFieldStack, MeasurementEntryGridField
from .MeasurementWidgets import UnitDisplay, UnitComboBox, UnitSpinBox
from .UnitComboDelegate import UnitComboDelegate
from .CurrentUnitSetter import setter as _setter
from . import SelectionMenu

_measurements = {}

def menu(parent, measurements=None):
    if measurements is None:
        #only those measurements which have been used for something
        return SelectionMenu.menu(_measurements.values(),parent)
    else:
        return SelectionMenu.menu([m for m in measurements if m in _measurements.values()], parent)

def Measurement(name):
    """
    :type name: str
    :rtype: MeasurementObject
    :raises UnitMeasurementException
    """
    if name not in _measurements:
        _measurements[name] = MeasurementObject(name)
    return _measurements[name]


def Unit(measurement, name):
    """
    :type measurement: MeasurementObject
    :type name: str
    :rtype: UnitObject
    :raises UnitMeasurementException
    """
    for u in measurement.units:
        if u.name == name:
            return u
    for u in measurement.units:
        if name in u.alias:
            return u
    raise UnitMeasurementException("There is no unit for " + str(measurement) + " by the name: " + name)

def changedSignal():
    """
    :rtype: callable
    """
    return _setter.changed

def measurements_list():
    return('Length','Angle','Pressure','Temperature','Volume', 'Mass', 'Proportion', 'Density', 'Force', 'Power', 'Time', 'AngularSpeed', 'Torque', 'None', 'Speed')