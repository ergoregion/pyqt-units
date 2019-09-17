
#Created on 14 Aug 2014

#@author: neil.butcher


from PySide2 import QtCore


class CurrentUnitSetter(QtCore.QObject):
    
    changed = QtCore.Signal(str,str,str)
    
    def setMeasurementUnit(self, m, u, label='normal'):
        """
        :type m: Measurement
        :type u: Unit
        :type label: str
        """
        m.setCurrentUnit(u, label)
        self.changed.emit(m.name, u.name, label)

setter = CurrentUnitSetter()  # Module wide item to transfer setting changes