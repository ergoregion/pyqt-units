"""
Created on 14 Apr 2016

@author: neil.butcher
"""

import sys
from PySide6 import QtWidgets
from pyqt_units import Measurement, menu


class MenuWidget(QtWidgets.QTableWidget):

    def __init__(self, parent = None):
        QtWidgets.QTableWidget.__init__(self, parent)


    def contextMenuEvent(self, event):

        m = menu(self)
        action = m.exec_(self.mapToGlobal(event.pos()))


class MenuWindow(QtWidgets.QMainWindow):

    def __init__(self,measurements):
        super(MenuWindow, self).__init__()
        w = MenuWidget(self)
        self.setCentralWidget(w)
        menubar = self.menuBar()
        m = menu(self,measurements)
        menubar.addMenu(m)

def main():
    length_measurement = Measurement('Length')
    time_measurement = Measurement('Time')
    speed_measurement = Measurement('Speed')

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MenuWindow([length_measurement,time_measurement])
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
