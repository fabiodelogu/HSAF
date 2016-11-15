"""
Library Features:

Name:          Lib_Data_IO_HDF5
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160708'
Version:       '1.5.0'
"""
#################################################################################
# Logging
import logging

oLogStream = logging.getLogger('sLogger')

import numpy as np

# Global libraries
from Drv_Exception import Exc
#################################################################################

# --------------------------------------------------------------------------------
# Method to open hdf5 file
def openFile(sFileName, sFileMode):
    import h5py

    try:
        # Open file
        oFile = h5py.File(sFileName, sFileMode)
        return oFile

    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_HDF5)' + ' [' + str(oError) + ']', 1, 1)

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close hdf5 file
def closeFile(oFile):
    Exc.getExc(' -----> Warning: no close method defined (Lib_Data_IO_HDF5)', 2, 1)
    pass

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to get variable by name
def getVar(oFile, sVarName):
    oVarData = oFile[str(sVarName)].value
    return oVarData
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to get all variable(s) by file handle
def getVars(oFile):

    oFileDict = {}
    for sDataSet in oFile:

        if isinstance(sDataSet, unicode):
            sDataSet = sDataSet.encode('utf8')
        else:
            pass

        oDataSet = oFile[sDataSet]
        oFileDict[sDataSet] = {}
        try:
            oFileDict[sDataSet] = oDataSet.value
        except:
            for sSubDataSet in oDataSet:

                if isinstance(sSubDataSet, unicode):
                    sSubDataSet = sSubDataSet.encode('utf8')
                else:
                    pass

                oFileDict[sDataSet][sSubDataSet] = {}
                oFileDict[sDataSet][sSubDataSet] = oDataSet[sSubDataSet].value
        finally:
            Exc.getExc(' -----> Warning: impossible to get selected variable (Lib_Data_IO_HDF5)', 2, 1)

    return oFileDict

# --------------------------------------------------------------------------------
