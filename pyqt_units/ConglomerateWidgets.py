"""
Created on 17 Aug 2014

@author: neil.butcher
"""

import sys

import MeasurementDatabase
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from MeasurementWidgets import UnitDisplay, UnitComboBox, UnitSpinBox


class UnitEntryField(QtGui.QWidget):
    valueChanged = pyqtSignal(float)

    def __init__(self, parent, measurement=None, measurementLabel='normal', label=None, delta=False, editableUnit=True):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setMargin(0)
        if not label == None:
            a = QtGui.QLabel(label, parent=self)
            self.layout.addWidget(a)
        self._box = UnitSpinBox(self, measurement, delta=delta, measurementLabel=measurementLabel)
        self._box.valueChanged.connect(self._valueChanged)
        self.layout.addWidget(self._box)
        self._measurement = measurement
        if editableUnit:
            self._unitfield = UnitComboBox(self, measurement, measurementLabel=measurementLabel)
        else:
            self._unitfield = UnitDisplay(self, measurement, measurementLabel=measurementLabel)
        self.layout.addWidget(self._unitfield)

    def _valueChanged(self, f):
        self.valueChanged.emit(f)

    def setMeasurement(self, measurement):
        self._measurement = measurement
        self._box.setMeasurement(measurement)
        self._unitfield.setMeasurement(measurement)

    def setMeasurementName(self, string):
        self.setMeasurement(MeasurementDatabase.Measurement(string))

    def value(self):
        return self._box.value()

    def setValue(self, f):
        return self._box.setValue(f)

    def setReadOnly(self, a_bool):
        self._box.setEnabled(not a_bool)

class SingleMeasurementEntryFieldStack(QtGui.QWidget):
    valueChanged = pyqtSignal(float, str)

    def __init__(self, parent, n=1, measurement=None, measurementLabel='normal', labels=None, deltas=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        signalMapper = QtCore.QSignalMapper(self)

        self.fields = [0] * n
        if labels is None:
            l = [None for _ in range(n)]
            self.identity = [str(i + 1) for i in range(n)]
        else:
            l = [str(i) for i in labels]
            self.identity = [str(i) for i in labels]
        if deltas is None:
            d = [None for _ in range(n)]
        else:
            d = deltas
        e = [False for _ in range(n)]
        e[0] = True

        for i in range(n):
            aField = UnitEntryField(self, measurement=measurement, measurementLabel=measurementLabel, label=l[i],
                                    delta=d[i], editableUnit=e[i])
            self.fields[i] = aField
            self.layout.addWidget(aField)
            aField.valueChanged.connect(signalMapper.map);
            signalMapper.setMapping(aField, i);

        signalMapper.mapped.connect(self._valueChanged)


    def setMeasurement(self, measurement):
        self._measurement = measurement
        for f in self.fields:
            f.setMeasurement(measurement)

    def _valueChanged(self, i):
        value = self.fields[i].value()
        identity = self.identity[i]
        print value, identity
        self.valueChanged.emit(value, identity)


class MeasurementEntryGridField(QtGui.QWidget):
    valueChanged = pyqtSignal(float, str)
    editingFinished = pyqtSignal(float, str)

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QGridLayout(self)
        self.layout.setMargin(2)
        self.layout.setSpacing(6)
        self.valueSignalMapper = QtCore.QSignalMapper(self)
        self.valueSignalMapper.mapped.connect(self._valueChanged)
        self.editingSignalMapper = QtCore.QSignalMapper(self)
        self.editingSignalMapper.mapped.connect(self._editingFinished)
        self.identifers = []
        self.boxes = []
        self.measurements = []

    def addField(self, measurement, identifer, measurementLabel='normal', label=None, delta=False, editable=None):
        nextIndex = len(self.identifers)
        if editable is None:
            _editable = (measurement, measurementLabel) not in self.measurements
        else:
            _editable = editable

        if not label is None:
            a = QtGui.QLabel(label, parent=self)
            a.setMargin(0)
            self.layout.addWidget(a, nextIndex, 0)

        _box = UnitSpinBox(self, measurement, measurementLabel=measurementLabel, delta=delta)
        _box.setMargin(0)
        self.layout.addWidget(_box, nextIndex, 1)
        _box.valueChanged.connect(self.valueSignalMapper.map)
        self.valueSignalMapper.setMapping(_box, nextIndex)
        _box.editingFinished.connect(self.editingSignalMapper.map)
        self.editingSignalMapper.setMapping(_box, nextIndex)
        self.boxes.append(_box)

        if _editable and measurement is not None:
            self._unitfield = UnitComboBox(self, measurement, measurementLabel=measurementLabel)
        else:
            self._unitfield = UnitDisplay(self, measurement, measurementLabel=measurementLabel)
        self._unitfield.setMargin(0)
        self.layout.addWidget(self._unitfield, nextIndex, 2)

        self.identifers.append(identifer)
        self.measurements.append((measurement, measurementLabel))


    def _valueChanged(self, i):
        value = self.boxes[i].value()
        identity = self.identifers[i]
        self.valueChanged.emit(value, identity)

    def _editingFinished(self, i):
        value = self.boxes[i].value()
        identity = self.identifers[i]
        self.editingFinished.emit(value, identity)

    def setValue(self, identity, value):
        i = self.identifers.index(identity, )
        value = self.boxes[i].setValue(value)

    def value(self, identity):
        i = self.identifers.index(identity, )
        return self.boxes[i].value()


