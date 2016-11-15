"""
Library Features:

Name:          Lib_Data_IO_Tiff
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160614'
Version:       '2.0.0'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
from Drv_Exception import Exc
#################################################################################

# --------------------------------------------------------------------------------
# Method to open Tiff file (in read or write mode)
def openFile(sFileName, sFileMode):
    from PIL import Image

    try:
        oFile = Image.open(sFileName, sFileMode)
        return oFile
    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_Tiff)' + ' [' + str(oError) + ']', 1, 1)

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close tiff file
def closeFile(oFile):
    oFile.close()
# --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Read 2d variable
def read2DVar(oFileData, iRowsRef, iColsRef):

    #----------------------------------------------------------------------------
    # Libraries
    import numpy as np

    # Check method
    try:

        #----------------------------------------------------------------------------
        # Get data
        a1oDataVar = list(oFileData.getdata())
        a1dDataVar = np.asarray(a1oDataVar, dtype=np.float32)
        a2dDataVar = np.reshape(a1dDataVar, (iRowsRef, iColsRef))
        a2dDataVar = np.flipud(a2dDataVar)

        return a2dDataVar
        #----------------------------------------------------------------------------

        # GDAL ...
        #oFileTiff = osgeo.gdal.Open(sFileNameTiff)
        #a2dDataVarInterp = np.zeros((iRowsRef, iColsRef))
        #a2dDataVarInterp = oFileTiff.ReadAsArray()
        #a2dDataVarInterp = np.flipud(a2dDataVarInterp)

    except:

        #----------------------------------------------------------------------------
        # Exit status with error
        Exc.getExc(' -----> ERROR: in read2DVar function (Lib_Data_IO_Tiff)', 1, 1)
        #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Convert tiff 2 ascii
def tiff2ascii(sFileNameTIFF, sFileNameASCII):

    #----------------------------------------------------------------------------
    # Libraries
    import subprocess

    # Check method
    try:

        sLineCommand = ('gdal_translate -of AAIGrid ' + sFileNameTIFF + ' ' + sFileNameASCII)

        oLogStream.info(sLineCommand)
        oPr = subprocess.Popen(sLineCommand, shell=True)
        oOut, oErr = oPr.communicate()

        return oOut, oErr

    except:

        #----------------------------------------------------------------------------
        # Exit status with error
        Exc.getExc(' -----> ERROR: in tiff2ascii function (Lib_Data_IO_Tiff)', 1, 1)
        #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------

#--------------------------------------------------------------------------------
