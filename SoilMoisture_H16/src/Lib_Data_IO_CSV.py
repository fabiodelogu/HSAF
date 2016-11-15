"""
Library Features:

Name:          Lib_Data_IO_CSV
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
# Method to open csv file
def openFile(sFileName, sFileMode):
    import csv

    try:
        oFileHandle = open(sFileName, sFileMode)

        if 'r' in sFileMode:
            oFile = csv.reader(oFileHandle)
        elif 'w' in sFileMode:
            oFile = csv.writer(oFileHandle, quoting=csv.QUOTE_NONNUMERIC)
        return oFile

    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_CSV)' + ' [' + str(oError) + ']', 1, 1)

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close csv file
def closeFile(oFile):
    Exc.getExc(' -----> Warning: no close method defined (Lib_Data_IO_CSV)', 2, 1)
    pass
# --------------------------------------------------------------------------------
