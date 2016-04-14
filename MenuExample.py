"""
Created on 14 Apr 2016

@author: neil.butcher
"""

import sys
from PyQt4 import QtGui, QtCore
from pyqt_units import Measurement, UnitEntryField, menu


class MenuWidget(QtGui.QTableWidget):

    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)
        length_measurement = Measurement('Length')
        time_measurement = Measurement('Time')
        speed_measurement = Measurement('Speed')



    def contextMenuEvent(self, event):

        m = menu(self)
        action = m.exec_(self.mapToGlobal(event.pos()))

def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = MenuWidget()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
