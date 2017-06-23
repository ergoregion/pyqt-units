
#Created on 14 Aug 2014

#@author: neil.butcher


from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal


class CurrentUnitSetter(QtCore.QObject):
    
    changed = pyqtSignal(str,str,str)
    
    def setMeasurementUnit(self, m, u, label='normal'):
        m.setCurrentUnit(u, label)
        self.changed.emit(m.name, u.name, label)

setter = CurrentUnitSetter()  # Module wide item to transfer setting changes