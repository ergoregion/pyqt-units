"""
Created on 14 Apr 2016

@author: neil.butcher
"""

import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal



def menu(measurements_list, parent):
    menu = QtGui.QMenu('Units', parent)

    for m in measurements_list:
        sm = _menu_for_measurement(m,menu)
        menu.addMenu(sm)

    return menu

def _menu_for_measurement(a_measurement, parent):
    m = QtGui.QMenu(a_measurement.name, parent)
    g = QtGui.QActionGroup(m)

    for u in a_measurement.units:
        a = _action_for_unit(u, m)
        g.addAction(a)
        m.addAction(a)

    return m


def _action_for_unit(a_unit, parent):

    action = QtGui.QAction(a_unit.name, parent)
    action.triggered.connect(a_unit.becomeCurrentNormalUnit)
    action.setCheckable(True)
    action.setChecked(a_unit is a_unit.currentUnit())
    return action