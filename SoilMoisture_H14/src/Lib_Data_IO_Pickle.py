"""
Library Features:

Name:          Lib_Data_IO_Pickle
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
# Method to open pickle file
def openFile(sFileName, sFileMode):
    import pickle

    try:
        if 'r' in sFileMode:
            oFile = pickle.load(open(sFileName, sFileMode + 'b'))
        elif 'w' in sFileMode:
            oFile = open(sFileName, sFileMode + 'b')
        return oFile

    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_Pickle)' + ' [' + str(oError) + ']', 1, 1)


# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close pickle file
def closeFile(oFile):
    Exc.getExc(' -----> Warning: no close method defined (Lib_Data_IO_Pickle)', 2, 1)
    pass
# --------------------------------------------------------------------------------
