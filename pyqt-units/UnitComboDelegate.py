"""
Created on 14 Aug 2014

@author: neil.butcher
"""

from PyQt4 import QtCore, QtGui


class UnitComboDelegate(QtGui.QStyledItemDelegate):
    
    def __init__(self, parent):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
    
        measurement = index.data(QtCore.Qt.UserRole).toPyObject()
        self.itemslist = measurement.units
        names_list = []
        for i in self.itemslist:
            names_list.append(i.name)
        self.editor = QtGui.QComboBox(parent)
        self.editor.addItems(names_list)
        self.editor.setCurrentIndex(0)
        self.editor.installEventFilter(self)    
        return self.editor

    def setEditorData(self, editor, index):
        text = index.data(QtCore.Qt.DisplayRole).toString()
        pos = self.editor.findText(text)
        if pos == -1:  
            pos = 0
        self.editor.setCurrentIndex(pos)
    
    def setModelData(self, editor, model, index):
        text = self.editor.currentText()
        i = self.editor.currentIndex()
        variant = QtCore.QVariant(text)
        variant.unit = self.itemslist[i]
        model.setData(index, variant)
    
    def updateEditorGeometry(self, editor, option, index):
        r = option.rect
        r.setSize(editor.sizeHint())
        self.editor.setGeometry(r)