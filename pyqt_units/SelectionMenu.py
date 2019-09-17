
#Created on 14 Apr 2016

#@author: neil.butcher

from PySide2 import QtWidgets


def menu(measurements_list, parent):
    menu = QtWidgets.QMenu('Units', parent)

    for m in measurements_list:
        sm = _menu_for_measurement(m,menu)
        menu.addMenu(sm)

    return menu

def _menu_for_measurement(a_measurement, parent):
    m = QtWidgets.QMenu(a_measurement.name, parent)
    g = QtWidgets.QActionGroup(m)

    for u in a_measurement.units:
        action = m.addAction(u.name, None)
        action.triggered.connect(u.becomeCurrentNormalUnit)
        action.setCheckable(True)
        action.setChecked(u is u.currentUnit())
        g.addAction(action)

    return m


def _action_for_unit(a_unit, parent):

    action = QtWidgets.QAction(a_unit.name, parent)
    action.triggered.connect(a_unit.becomeCurrentNormalUnit)
    action.setCheckable(True)
    action.setChecked(a_unit is a_unit.currentUnit())
    return action