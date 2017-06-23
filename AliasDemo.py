from pyqt_units import Measurement, Unit

m = Measurement('Length')

u =Unit(m,'mm')
print(u.scale)