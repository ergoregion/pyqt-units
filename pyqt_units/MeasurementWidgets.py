
#Created on 14 Aug 2014

#@author: neil.butcher


from PySide6 import QtCore, QtWidgets
from pyqt_units.CurrentUnitSetter import setter


class UnitDisplay(QtWidgets.QWidget):
    def __init__(self, parent, measurement=None, measurementLabel='normal'):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QVBoxLayout()
        self._label = QtWidgets.QLabel('', self)
        self.layout.addWidget(self._label)
        self.layout.setMargin(2)
        self.measurement = measurement
        self._measurementLabel = measurementLabel
        setter.changed.connect(self.currentUnitChangedElsewhere)
        self._update()

    @QtCore.Slot(str, str, str)
    def currentUnitChangedElsewhere(self, measName, unitName, measurementLabel):
        if self.measurement == None:
            pass
        elif not measName == self.measurement.name:
            pass
        elif not measurementLabel == self._measurementLabel:
            pass
        else:
            self._updateText(unitName)

    def setMeasurement(self, measurement):
        self.measurement = measurement
        self._update()

    def setMargin(self, margin):
        self.layout.setMargin(margin)

    def _update(self):
        if self.measurement == None:
            self._updateText('')
        else:
            self._updateText(self.measurement.currentUnit(label=self._measurementLabel).name)

    def _updateText(self, txt):
        self._label.setText(txt)


class UnitComboBox(QtWidgets.QWidget):
    def __init__(self, parent, measurement=None, measurementLabel='normal'):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setMargin(2)
        self._box = QtWidgets.QComboBox(self)
        self.layout.addWidget(self._box)
        self._measurementLabel = measurementLabel
        self._box.currentIndexChanged.connect(self.changedToIndex)
        setter.changed.connect(self.currentUnitChangedElsewhere)
        self.setMeasurement(measurement)
        self._update()

    @QtCore.Slot(str, str, str)
    def currentUnitChangedElsewhere(self, measName, unitName, measurementLabel):
        if self.measurement == None:
            pass
        elif not measName == self.measurement.name:
            pass
        elif not measurementLabel == self._measurementLabel:
            pass
        else:
            self._update()

    def setMeasurement(self, measurement):
        self.measurement = None
        self._box.clear()
        if measurement is None:
            pass
        else:
            self.itemslist = measurement.units
            namesList = []
            for i in self.itemslist:
                namesList.append(i.name)
            self._box.addItems(namesList)
        self.measurement = measurement
        self._update()

    def setMargin(self, margin):
        self.layout.setMargin(margin)

    def _update(self):
        if self.measurement is None:
            pass
        else:
            text = self.measurement.currentUnit(label=self._measurementLabel).name
            pos = self._box.findText(text)
            if pos == -1:
                pos = 0
            self._box.setCurrentIndex(pos)

    @QtCore.Slot(int)
    def changedToIndex(self, i):
        if not self.measurement == None:
            unit = self.itemslist[i]
            setter.setMeasurementUnit(self.measurement, unit, self._measurementLabel)


class AddaptiveDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def textFromValue(self, value):
        s = '{0:g}'.format(value)
        return s


class UnitSpinBox(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)
    editingFinished = QtCore.Signal()

    def __init__(self, parent, measurement=None, delta=False, measurementLabel='normal'):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setMargin(2)
        self._box = AddaptiveDoubleSpinBox(self)
        self._box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self._box.setMaximum(2.0e30)
        self._box.setMinimum(-2.0e30)
        self._box.setDecimals(12)
        self.layout.addWidget(self._box)
        self._box.valueChanged.connect(self._valueChanged)
        self._box.editingFinished.connect(self._editingFinished)
        setter.changed.connect(self.currentUnitChangedElsewhere)
        self.delta = delta
        self._baseValue = None
        self._measurementLabel = measurementLabel
        self.setMeasurement(measurement)
        self._update()

    @QtCore.Slot(str, str, str)
    def currentUnitChangedElsewhere(self, measName, unitName, measurementLabel):
        if self.measurement is None:
            pass
        elif not measName == self.measurement.name:
            pass
        elif not measurementLabel == self._measurementLabel:
            pass
        else:
            self._update()

    def setMeasurement(self, measurement):
        self.measurement = measurement
        self._update()

    def setMargin(self, margin):
        self.layout.setMargin(margin)

    def unit(self):
        return self.measurement.currentUnit(label=self._measurementLabel)

    def _update(self):
        if self._baseValue is None:
            self._box.clear()
        elif self.measurement is None:
            self._box.setValue(self._baseValue)
        elif self.delta:
            scaledValue = self.unit().scaledDeltaValueOf(self._baseValue)
            self._box.setValue(scaledValue)
        else:
            scaledValue = self.unit().scaledValueOf(self._baseValue)
            self._box.setValue(scaledValue)

    def setValue(self, baseValue):
        self._baseValue = baseValue
        self._update()

    def _valueChanged(self, scaledValue):
        if scaledValue is None:
            newValue = None
        elif self.measurement is None:
            newValue = scaledValue
        elif self.delta:
            newValue = self.unit().baseDeltaValueFrom(scaledValue)
        else:
            newValue = self.unit().baseValueFrom(scaledValue)

        a = self._baseValue
        b = newValue
        if a is None or abs(a - b) > max(abs(a), abs(b)) * 1e-8:
            self._baseValue = newValue
            self.valueChanged.emit(self._baseValue)

    def _editingFinished(self):
        self.editingFinished.emit()

    def value(self):
        return self._baseValue