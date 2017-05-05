# -*- coding:utf-8 -*-
# program name: H5toTXT.py
#
import os
import sys
import h5py

os.chdir(sys.path[0])

TransientHDF5FileName = 'TransientCTF.h5'

TransientHDF5File = h5py.File(TransientHDF5FileName,'a')

