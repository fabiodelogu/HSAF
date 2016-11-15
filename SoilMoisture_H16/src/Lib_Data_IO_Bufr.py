"""
Library Features:

Name:          Lib_Data_IO_Bufr
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20161010'
Version:       '2.0.1'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
from Drv_Exception import Exc
#################################################################################

# --------------------------------------------------------------------------------
# Method to open bufr file
def openFile(sFileName):
    # Import library
    import bufr

    # `Check method
    try:
        # Open file
        oFile = bufr.BUFRFile(sFileName)
        return oFile
    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_Bufr)' + ' [' + str(oError) + ']', 1, 1)

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close/delete bufr file handle
def closeFile(oFile):
    del oFile
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to rewind at beginning bufr file
def rewindFile(oFile):
    oFile.reset()
    return oFile
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Read ArcGrid data
def readData(oFileData, sVarName=None):

    # ----------------------------------------------------------------------------
    # Library
    import numpy as np
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Check method
    try:

        # ----------------------------------------------------------------------------
        # Removing leading and trailing blanks from name
        sVarName = sVarName.strip()
        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        # Cycle(s) on field(s)
        a1dVarValue_Tot = np.array([])
        for a1oFileField in oFileData:

            # ----------------------------------------------------------------------------
            # Un-packing all records in file
            for a1oFileRecord in a1oFileField:

                # ----------------------------------------------------------------------------
                # Selection of bufr variable
                sFileVar = a1oFileRecord.name
                sFileVar = sFileVar.strip()
                # ----------------------------------------------------------------------------

                # ----------------------------------------------------------------------------
                # Check selected variable
                if sVarName:

                    # Check variable name
                    if sVarName == sFileVar:

                        # Get variable value(s)
                        a1dVarValue_Step = []
                        a1dVarValue_Step = a1oFileRecord.data

                        # Save variable value(s)
                        if a1dVarValue_Tot is None:
                            a1dVarValue_Tot = a1dVarValue_Step
                        else:
                            a1dVarValue_Tot = np.concatenate((a1dVarValue_Tot, a1dVarValue_Step), axis=0)

                    else:
                        pass

                else:
                    Exc.getExc(' -----> ERROR: in readData function (Lib_Data_IO_Bufr); Undefined function arguments VarName', 1, 1)
                # ----------------------------------------------------------------------------

            # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        # Save variable value(s)
        return a1dVarValue_Tot
        # ----------------------------------------------------------------------------

    except:

        # ----------------------------------------------------------------------------
        # Exit status with error
        a1dVarValue_Tot = np.array([])
        Exc.getExc(' -----> WARNING: error in readData function (Lib_Data_IO_Bufr)', 2, 1)
        return a1dVarValue_Tot
        # ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
