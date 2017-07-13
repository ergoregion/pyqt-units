from pyqt_units import Measurement, Unit

m = Measurement('Length')
m.addAlias('wewe')

m= Measurement('wewe')

u =Unit(m,'mm')
print(u.scale)

#note this can only be run once before you have to delete the temp database
u.addAlias('ddff')

k =Unit(m,'ddff')
print(k.scale)