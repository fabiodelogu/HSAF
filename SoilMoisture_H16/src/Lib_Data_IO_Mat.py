"""
Library Features:

Name:          Lib_Data_IO_Mat
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
# Method to open mat file (in read mode)
def openFile(sFileName):
    import scipy.io

    try:
        oFile = scipy.io.loadmat(sFileName)
        return oFile
    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_Mat)' + ' [' + str(oError) + ']', 1, 1)

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#  Method to close grib file
def closeFile(oFile):
    Exc.getExc(' -----> Warning: no close method defined (Lib_Data_IO_CSV)', 2, 1)
    pass
# --------------------------------------------------------------------------------
