"""
Created on 16 Mar 2016

@author: neil.butcher
"""

import sys
from PySide2 import QtWidgets
from pyqt_units import Measurement, UnitEntryField


class CalculationWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None)
        self.layout = QtWidgets.QVBoxLayout()

        length_measurement = Measurement('Length')
        time_measurement = Measurement('Time')
        speed_measurement = Measurement('Speed')

        self.distance_entry_widget = UnitEntryField(self, measurement=length_measurement, label="Distance")
        self.distance_entry_widget.valueChanged.connect(self._update_calculation)
        self.layout.addWidget(self.distance_entry_widget)

        self.time_entry_widget = UnitEntryField(self, measurement=time_measurement, label="Time")
        self.time_entry_widget.valueChanged.connect(self._update_calculation)
        self.layout.addWidget(self.time_entry_widget)

        self.speed_reporting_widget = UnitEntryField(self, measurement=speed_measurement, label="Speed")
        self.speed_reporting_widget.setReadOnly(True)
        self.layout.addWidget(self.speed_reporting_widget)

        # due to the use of the widgets to handle units we can always set values in SI units
        self.distance_entry_widget.setValue(1.0)  # 1 meter
        self.time_entry_widget.setValue(1.0)  # 1 second
        self._update_calculation()

    def _update_calculation(self):
        # due to the use of the widgets to handle units the values retrieved will always be in SI units
        distance = self.distance_entry_widget.value()
        time = self.time_entry_widget.value()

        # we can perform a unit-free SI calculation
        speed = distance / time

        # and set the value in SI units, the widget will change text to reflect units
        self.speed_reporting_widget.setValue(speed)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = CalculationWidget()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
