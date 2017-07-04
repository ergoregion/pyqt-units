
#Created on 12 Aug 2014

#@author: neil.butcher

import os
from shutil import copyfile
root_filename =  os.path.join(os.path.dirname(__file__) , 'measurements' ,'measurements_root.db')

filename = os.path.join(os.path.dirname(__file__) , 'measurements' , 'measurements_temp.db')

if not os.path.isfile(filename):
    copyfile(root_filename,filename)

