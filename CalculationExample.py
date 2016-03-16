"""
Created on 16 Mar 2016

@author: neil.butcher
"""

import sys
from PyQt4 import QtGui
from pyqt_units import Measurement, UnitEntryField



class CalculationWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self, None)
        self.layout = QtGui.QVBoxLayout(self)

        length_measurement = Measurement('Length')
        time_measurement = Measurement('Time')
        speed_measurement = Measurement('Length')

        self.distance_entry_widget = UnitEntryField(self, measurement=length_measurement, label="Distance")
        self.distance_entry_widget.valueChanged.connect(self._update_calculation)
        self.layout.addWidget(self.distance_entry_widget)

        self.time_entry_widget = UnitEntryField(self, measurement=time_measurement, label="Time")
        self.time_entry_widget.valueChanged.connect(self._update_calculation)
        self.layout.addWidget(self.time_entry_widget)

        self.speed_reporting_widget = UnitEntryField(self, measurement=speed_measurement, label="Speed")
        self.layout.addWidget(self.speed_reporting_widget)


    def _update_calculation(self):
        distance = self.distance_entry_widget.value()
        time = self.time_entry_widget.value()
        speed = distance / time

        self.speed_reporting_widget.setValue(speed)



def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = CalculationWidget()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()