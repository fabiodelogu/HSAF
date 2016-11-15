"""
Library Features:

Name:          Lib_Geo_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160628'
Version:       '1.0.0'
"""

#################################################################################
# Logging
import logging

oLogStream = logging.getLogger('sLogger')

import numpy as np

from Drv_Exception import Exc

# Debug
# import matplotlib.pylab as plt
#################################################################################

# --------------------------------------------------------------------------------
# Method to find XY geographical indexes
def findGeoIndex(a2dGeoX_REF, a2dGeoY_REF, a2dGeoX_VAR, a2dGeoY_VAR, dGeoCellSize_VAR):

    # Get geographical information
    dYU_REF = np.max(a2dGeoY_REF)
    dXL_REF = np.min(a2dGeoX_REF)
    # Compute index
    a1dIndexY_VAR = np.ceil((dYU_REF - a2dGeoY_VAR.revel()) / dGeoCellSize_VAR)
    a1dIndexX_VAR = np.ceil((a2dGeoX_VAR.revel() - dXL_REF) / dGeoCellSize_VAR)
    # From double to integer
    a1iIndexX_VAR = np.int32(a1dIndexX_VAR)
    a1iIndexY_VAR = np.int32(a1dIndexY_VAR)

    return a1iIndexX_VAR, a1iIndexY_VAR
# --------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Method to check domains are equal feature(s)
def checkGeoDomain(oGeoHeader_VAR=None, oGeoHeader_REF=None):

    a1bVarCheck = {}
    for sVarName_VAR, oVarValue_VAR in oGeoHeader_VAR.iteritems():
        if sVarName_VAR in oGeoHeader_REF:
            oVarValue_REF = oGeoHeader_REF[sVarName_VAR]
            if oVarValue_VAR == oVarValue_REF:
                a1bVarCheck[sVarName_VAR] = True
            else:
                a1bVarCheck[sVarName_VAR] = False
        else:
            a1bVarCheck[sVarName_VAR] = False

    if all(a1bVarCheck.values()):
        bVarCheck = True
    else:
        bVarCheck = False

    return bVarCheck

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Method to read geographical box
def readGeoBox(a1oGeoBox):

    dGeoXMin = a1oGeoBox['xllcorner']
    dGeoYMin = a1oGeoBox['yllcorner']
    dGeoXMax = a1oGeoBox['xurcorner']
    dGeoYMax = a1oGeoBox['yurcorner']
    dGeoXStep = a1oGeoBox['xcellsize']
    dGeoYStep = a1oGeoBox['ycellsize']

    if 'nrows' in a1oGeoBox:
        iRows = a1oGeoBox['nrows']
    else:
        iRows = int(np.round((dGeoYMax - dGeoYMin) / dGeoYStep + 1))

    if 'ncols' in a1oGeoBox:
        iCols = a1oGeoBox['ncols']
    else:
        iCols = int(np.round((dGeoXMax - dGeoXMin) / dGeoXStep + 1))

    return iRows, iCols, dGeoXMin, dGeoYMin, dGeoXMax, dGeoYMax, dGeoXStep, dGeoYStep

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Method to define geographical box
def defineGeoBox(dGeoXMin, dGeoYMin, dGeoXMax, dGeoYMax, dGeoXStep, dGeoYStep):

    iCols = int(np.round((dGeoXMax - dGeoXMin) / dGeoXStep + 1))
    iRows = int(np.round((dGeoYMax - dGeoYMin) / dGeoYStep + 1))

    a1oGeoBox = {'xllcorner': dGeoXMin, 'xurcorner': dGeoXMax, 'yllcorner': dGeoYMin, 'yurcorner': dGeoYMax,
                 'xcellsize': dGeoXStep, 'ycellsize': dGeoYStep, 'nrows': iRows, 'ncols': iCols}

    return a1oGeoBox

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Method to read header of geographical data
def readGeoHeader(a1oGeoHeader):

    iRows = a1oGeoHeader['nrows']
    iCols = a1oGeoHeader['ncols']
    dGeoXMin = a1oGeoHeader['xllcorner']
    dGeoYMin = a1oGeoHeader['yllcorner']
    dGeoXStep = a1oGeoHeader['cellsize']
    dGeoYStep = a1oGeoHeader['cellsize']
    dNoData = a1oGeoHeader['NODATA_value']

    return iRows, iCols, dGeoXMin, dGeoYMin, dGeoXStep, dGeoYStep, dNoData

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Method to define header of geographical data
def defineGeoHeader(iRows, iCols, dGeoXMin, dGeoYMin, dGeoXStep, dGeoYStep, dNoData):

    a1oGeoHeader = {'nrows': iRows, 'ncols': iCols, 'xllcorner': dGeoXMin,
                    'cellsize': dGeoXStep, 'yllcorner': dGeoYMin,
                    'NODATA_value': dNoData}

    return a1oGeoHeader
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Method to define goegraphical corners (geox min, geox max, geoy min and geoy max)
def defineGeoCorner(dGeoXMin, dGeoYMin, dGeoXStep, dGeoYStep, iCols, iRows):

    # Define geographical cell center
    dGeoXMin = dGeoXMin + dGeoXStep / 2.
    dGeoYMin = dGeoYMin + dGeoYStep / 2.

    # Compute
    dGeoXMax = dGeoXMin + (iCols - 1) * dGeoXStep
    dGeoYMax = dGeoYMin + (iRows - 1) * dGeoYStep

    return dGeoXMin, dGeoXMax, dGeoYMin, dGeoYMax

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Method to define geographical information (geox, geoy, geobox)
def defineGeoGrid(dGeoYMin, dGeoXMin, dGeoYMax, dGeoXMax, dGeoYStep, dGeoXStep):

    # -------------------------------------------------------------------------------------
    # Creating geox and geoy references
    a1dGeoX = np.arange(dGeoXMin, dGeoXMax + np.abs(dGeoXStep / 2), np.abs(dGeoXStep), float)
    a1dGeoY = np.arange(dGeoYMin, dGeoYMax + np.abs(dGeoYStep / 2), np.abs(dGeoYStep), float)

    a2dGeoX, a2dGeoY = np.meshgrid(a1dGeoX, a1dGeoY)
    a2dGeoY = np.flipud(a2dGeoY)

    dGeoXMin = np.nanmin(a2dGeoX)
    dGeoXMax = np.nanmax(a2dGeoX)
    dGeoYMax = np.nanmax(a2dGeoY)
    dGeoYMin = np.nanmin(a2dGeoY)
    oGeoBox = [dGeoXMin, dGeoYMax, dGeoXMax, dGeoYMin]

    a1dGeoBox = np.around(oGeoBox, decimals=3)

    return a2dGeoX, a2dGeoY, a1dGeoBox
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to convert curve number to maximum volume
def computeCN2VMax(a2dDataCN):

    # Initialize VMax 2D array
    a2dDataVMax = np.zeros([a2dDataCN.shape[0], a2dDataCN.shape[1]])
    a2dDataVMax[:, :] = np.nan

    # Compute VMax starting from Curve Number values
    a2dDataVMax = (1000/a2dDataCN - 10) * 25.4

    #a2dMapVMax(a1iIndexNanCN) = NaN;

    return a2dDataVMax

# --------------------------------------------------------------------------------
