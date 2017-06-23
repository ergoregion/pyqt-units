
#Created on 12 Aug 2014

#@author: neil.butcher

import os
from shutil import copyfile
root_filename =  os.path.dirname(__file__) + '/Measurements/Measurements_root.db'

filename = 'Measurements_temp.db'

if not os._exists(filename):
    copyfile(root_filename,filename)
