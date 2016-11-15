"""
Library Features:

Name:          Lib_Data_Zip_BZ2
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160726'
Version:       '2.0.0'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import bz2

# Global libraries
from Drv_Exception import Exc
#################################################################################

# --------------------------------------------------------------------------------
# Method to open bz2 file
def openZip(sFileName_IN, sFileName_OUT, sZipMode):

    # Check method
    try:

        # Open file
        if sZipMode == 'z':  # zip mode
            oFile_IN = open(sFileName_IN, 'rb')
            oFile_OUT = bz2.BZ2File(sFileName_OUT, 'wb')
        elif sZipMode == 'u':  # unzip mode
            oFile_IN = bz2.BZ2File(sFileName_IN)
            oFile_OUT = open(sFileName_OUT, "wb")

        # Pass file handle(s)
        return oFile_IN, oFile_OUT

    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (BZ2 Zip)' + ' [' + str(oError) + ']', 1, 1)

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close bufr file
def closeZip(oFile_IN=None, oFile_OUT=None):
    if oFile_IN:
        oFile_IN.close()
    if oFile_OUT:
        oFile_OUT.close()
# --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to check if zip file is corrupted or not
def checkZip(sFileName):
    try:
        oFileTest = bz2.BZ2File(sFileName).read()
        bFileCheck = True
    except:
        Exc.getExc(' -----> WARNING: errors occurred in checking file integrity (BZ2 Zip)', 2, 1)
        bFileCheck = False

    return bFileCheck
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to zip file
def zipFile(oFile_IN=None, oFile_OUT=None):
    if oFile_IN and oFile_OUT:
        oFile_OUT.writelines(oFile_IN)
    else:
        Exc.getExc(' -----> ERROR: in zip file (BZ2 Zip)', 1, 1)
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to unzip file
def unzipFile(oFile_IN=None, oFile_OUT=None):
    if oFile_IN and oFile_OUT:
        try:
            oDecompressData = oFile_IN.read()
            oFile_OUT.write(oDecompressData)
        except:
            Exc.getExc(' -----> WARNING: errors occurred in unzipping file (BZ2 Zip)', 2, 1)
    else:
        Exc.getExc(' -----> ERROR: in unzip file (BZ2 Zip)', 1, 1)
#--------------------------------------------------------------------------------
