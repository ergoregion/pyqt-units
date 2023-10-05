import sys
from PySide6 import QtWidgets
from pyqt_units import Measurement


class PrintWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.length_measurement = Measurement('Length')

        self.text_entry_widget = QtWidgets.QLineEdit(self)
        self.text_entry_widget.textChanged.connect(self._print_text)
        self.layout.addWidget(self.text_entry_widget)

        self.spin_entry_widget = QtWidgets.QSpinBox(self)
        self.spin_entry_widget.valueChanged.connect(self._print_float)
        self.layout.addWidget(self.spin_entry_widget)

    def _print_text(self):
        text = self.text_entry_widget.text()
        print (self.length_measurement.report(text))

    def _print_float(self):
        float = self.spin_entry_widget.value()
        print (self.length_measurement.report(float))



def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = PrintWidget()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
