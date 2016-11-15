"""
Library Features:

Name:          Lib_Data_Zip_GZip
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160616'
Version:       '2.0.0'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import gzip

# Global libraries
from Drv_Exception import Exc
#################################################################################


# --------------------------------------------------------------------------------
# Method to open bufr file
def openZip(sFileName_IN, sFileName_OUT, sZipMode):

    # Check method
    try:

        # Open file
        if sZipMode == 'z':  # zip mode
            oFile_IN = open(sFileName_IN, 'rb')
            oFile_OUT = gzip.open(sFileName_OUT, 'wb')
        elif sZipMode == 'u':  # unzip mode
            oFile_IN = gzip.GzipFile(sFileName_IN, "rb")
            oFile_OUT = open(sFileName_OUT, "wb")

        # Pass file handle(s)
        return oFile_IN, oFile_OUT

    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (GZip Zip)' + ' [' + str(oError) + ']', 1, 1)

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
# Method to zip file
def zipFile(oFile_IN=None, oFile_OUT=None):
    if oFile_IN and oFile_OUT:
        oFile_OUT.writelines(oFile_IN)
    else:
        Exc.getExc(' -----> ERROR: in zip file (GZip Zip)', 1, 1)
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to unzip file
def unzipFile(oFile_IN=None, oFile_OUT=None):
    if oFile_IN and oFile_OUT:
        oDecompressData = oFile_IN.read()
        oFile_OUT.write(oDecompressData)
    else:
        Exc.getExc(' -----> ERROR: in unzip file (GZip Zip)', 1, 1)
#--------------------------------------------------------------------------------
