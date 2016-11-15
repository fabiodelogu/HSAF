"""
Library Features:

Name:          Lib_Data_IO_HDF4
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160805'
Version:       '1.5.0'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
from Drv_Exception import Exc
#################################################################################

# --------------------------------------------------------------------------------
# Method to open hdf4 file
def openFile(sFileName):
    from osgeo import gdal

    # `Check method
    try:
        # Open file
        oFile = gdal.Open(sFileName)
        return oFile

    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_HDF4)' + ' [' + str(oError) + ']', 1, 1)

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close hdf4 file
def closeFile(oFile):
    Exc.getExc(' -----> Warning: no close method defined (Lib_Data_IO_HDF4)', 2, 1)
    pass

# --------------------------------------------------------------------------------
