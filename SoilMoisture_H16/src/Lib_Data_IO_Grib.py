"""
Library Features:

Name:          Lib_Data_IO_Grib
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160726'
Version:       '2.0.0'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import pygrib
import numpy as np

# Global libraries
from Drv_Exception import Exc

#import matplotlib.pylab as plt
#################################################################################

#--------------------------------------------------------------------------------
# Method to open grib file
def openFile(sFileName):

    # Open file
    try:
        oFile = pygrib.open(sFileName)
        return oFile
    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (GRIB I/O)' + ' [' + str(oError) + ']', 1, 1)

#--------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close grib file
def closeFile(oFile):
    pass
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to check messages in file
def checkFileMessage(oFile=None, iAttMessage=0):
    if oFile:
        iFileMessages = oFile.messages

        if iAttMessage == iFileMessages:
            bFileCheck = True
        else:
            bFileCheck = False
    else:
        bFileCheck = False
    return bFileCheck
# --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to read 2d variable
def readVar2D(oFile, iIndex):

    #----------------------------------------------------------------------------
    # Check method
    try:
        # ----------------------------------------------------------------------------
        # Read variable using data index
        oVar = oFile[iIndex]
        a2dVarData_Masked = oVar.values
        a2dVarData = a2dVarData_Masked.data

        return a2dVarData
        # ----------------------------------------------------------------------------
    except:
        #----------------------------------------------------------------------------
        # Exit status with error
        Exc.getExc(' -----> WARNING: in read2DVar function (Lib_Data_IO_Grib)', 2, 1)
        #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to read geographical variable
def readVarGeo(oFile, iIndex):
    [a2dGeoY, a2dGeoX] = oFile[iIndex].latlons()
    return a2dGeoX, a2dGeoY
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to check variable(s) orientation (O-E, S-N)
def checkVarOrient(a2dVarData, a2dVarGeoX, a2dVarGeoY):

    dVarGeoY_LL = a2dVarGeoY[a2dVarGeoY.shape[0] - 1, 0]
    dVarGeoY_UL = a2dVarGeoY[0, 0]
    #dVarGeoY_UR = a2dVarGeoY[0, a2dVarGeoY.shape[1] - 1]
    #dVarGeoY_LR = a2dVarGeoY[a2dVarGeoY.shape[0] - 1, a2dVarGeoY.shape[1] - 1]

    # Debug
    #print(dVarGeoY_LL, dVarGeoY_UL, dVarGeoY_UR, dVarGeoY_LR)
    #plt.figure(1)
    #plt.imshow(a2dVarGeoY)
    #plt.colorbar()
    #plt.show()

    if dVarGeoY_LL > dVarGeoY_UL:
        a2dVarGeoY = np.flipud(a2dVarGeoY)
        a2dVarData = np.flipud(a2dVarData)
    else:
        pass

    return a2dVarData, a2dVarGeoX, a2dVarGeoY

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to print variable attributes
def printVarAttrs(oFile):
    for oData in oFile:
        print oData.typeOfLevel, oData.level, oData.name, oData.validDate, oData.analDate, oData.forecastTime
# --------------------------------------------------------------------------------
