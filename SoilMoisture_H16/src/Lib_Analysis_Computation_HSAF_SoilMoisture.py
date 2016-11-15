"""
Library Features:

Name:          Lib_Analysis_Computation_HSAF_SM
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20161004'
Version:       '1.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import numpy as np

from Drv_Exception import Exc

# Debug
#import matplotlib.pylab as plt
#################################################################################

# --------------------------------------------------------------------------------
# Method to compute minimum values along axis
def computeVarMin(a2dVarData, iAxis=1):
    a1dVarData = np.nanmin(a2dVarData, axis=iAxis)
    return a1dVarData
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute maximum values along axis
def computeVarMax(a2dVarData, iAxis=1):
    a1dVarData = np.nanmax(a2dVarData, axis=iAxis)
    return a1dVarData
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute average values along axis
def computeVarMean(a2dVarData, iAxis=1):
    a1dVarData = np.nanmean(a2dVarData, axis=iAxis)
    return a1dVarData
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute standard deviation values along axis
def computeVarStDev(a2dVarData, iAxis=1):
    a1dVarData = np.nanstd(a2dVarData, axis=iAxis)
    return a1dVarData
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute variable linear rescaling
def computeVarLinScale(a2dVarData, a2dVarMean, a2dVarStDev, a2dModelMean, a2dModelStDev):

    a2dVarLRS = ((a2dVarData - a2dVarMean) / a2dVarStDev) * a2dModelStDev + a2dModelMean

    #plt.figure(1)
    #plt.imshow(oModelStDev); plt.colorbar()
    #plt.figure(2)
    #plt.imshow(oModelMean); plt.colorbar()
    #plt.figure(3)
    #plt.imshow(oVarStDev); plt.colorbar()
    #plt.figure(4)
    #plt.imshow(oVarMean); plt.colorbar()
    #plt.figure(5)
    #plt.imshow(oVarData); plt.colorbar()

    #plt.figure(6)
    #plt.imshow(oVarLRS); plt.colorbar()
    #plt.show()

    return a2dVarLRS
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute variable min-max normalization
def computeVarNormMinMax(a2dVarData, a2dVarMin, a2dVarMax):
    a2dVarNMM = (a2dVarData - a2dVarMin) / (a2dVarMax - a2dVarMin)
    return a2dVarNMM

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute variable min-max normalization
def computeVarSM_Lev1(a2dVarDataL1):

    # Equation: float(7)/float(7)*H14_SM_V_L1
    a2dVarDataL1_INT = (np.float(7.0) / np.float(7.0)) * a2dVarDataL1
    return a2dVarDataL1_INT

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute variable min-max normalization
def computeVarSM_Lev2(a2dVarDataL1, a2dVarDataL2):

    # Equation: float(7)/float(28)*H14_SM_V_L1 + float(28-7)/float(28)*H14_SM_V_L2
    a2dVarDataL2_INT = ((np.float(7.0) / np.float(28.0)) * a2dVarDataL1 +
                        (np.float(28.0 - 7.0) / np.float(28.0)) * a2dVarDataL2)
    return a2dVarDataL2_INT

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute variable min-max normalization
def computeVarSM_Lev3(a2dVarDataL1, a2dVarDataL2, a2dVarDataL3):

    # Equation: float(7)/float(100)*H14_SM_V_L1 + float(28-7)/float(100)*H14_SM_V_L2 + (float(100-7-(28-7))/float(100))*H14_SM_V_L3
    a2dVarDataL3_INT = ((np.float(7.0) / np.float(100.0)) * a2dVarDataL1 +
                        (np.float(28.0 - 7.0) / np.float(100.0)) * a2dVarDataL2 +
                        (np.float(100.0 - 7.0 - (28.0 - 7.0)) / np.float(100.0)) * a2dVarDataL3)
    return a2dVarDataL3_INT

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute variable min-max normalization
def computeVarSM_Lev4(a2dVarDataL1, a2dVarDataL2, a2dVarDataL3, a2dVarDataL4):

    # Equation: 1*H14_SM_V_L1 + 1*H14_SM_V_L2 + 1*H14_SM_V_L3 + 1*H14_SM_V_L4
    a2dVarDataL4_INT = ((np.float(1.0)) * a2dVarDataL1 +
                        (np.float(1.0)) * a2dVarDataL2 +
                        (np.float(1.0)) * a2dVarDataL3 +
                        (np.float(1.0)) * a2dVarDataL4)
    return a2dVarDataL4_INT

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute soil water index (SWI)
def computeVarSWI(a2dVarData=None, a1oVarTime=None, iTimeFilter=None, sTimeFrom=None, sTimeTo=None):

    # -------------------------------------------------------------------------------------
    # Libraries
    from copy import deepcopy
    from datetime import datetime
    from time import mktime
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Time index to select period of data
    iIndexFrom = a1oVarTime.index(sTimeFrom)
    iIndexTo = a1oVarTime.index(sTimeTo)

    # Data selection
    a2dVarData_SEL = a2dVarData[:, iIndexFrom: iIndexTo]
    a1dVarDims_SEL = a2dVarData_SEL.shape
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Cycle(s) on each row
    a2dVarSWI = np.zeros((a1dVarDims_SEL[0], a1dVarDims_SEL[1]))
    for iP in range(0, a1dVarDims_SEL[0]):

        # -------------------------------------------------------------------------------------
        # Select data for each row and in time period
        a1dVarData_SEL = a2dVarData_SEL[iP, :]
        if np.any(np.isfinite(a1dVarData_SEL[:])):

            # -------------------------------------------------------------------------------------
            # Undefined but not null value at actual step if value is not defined
            # Due to calculate propagation of recursive filter on end day if has not observed value
            if np.isnan(a1dVarData_SEL[-1]):
                a1dVarData_SEL[-1] = -1  # Switch condition if value is >=0
            else:
                pass
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Compute data selection length
            iVarDim_SEL = len(a1dVarData_SEL)

            # Time series finite values and indexes
            a1iDV = np.where(np.isfinite(a1dVarData_SEL[:]) == True)[0]
            iDV_VALID = len(a1iDV)
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Cycle(s) on finite values and Kn and SWI initialization
            a1dVarKN = np.ones((1, iVarDim_SEL))
            a1dVarSWI_STEP = deepcopy(a1dVarData_SEL)
            for iL in range(1, iDV_VALID):

                # -------------------------------------------------------------------------------------
                # Start and end indexes
                iIndexDV_END = a1iDV[iL]
                iIndexDV_START = a1iDV[iL - 1]

                # Defining start and end dates
                iDV_END = int(a1oVarTime[iIndexDV_END])
                oDV_END = datetime.strptime(str(iDV_END), '%Y%m%d%H%M%S')

                iDV_START = int(a1oVarTime[iIndexDV_START])
                oDV_START = datetime.strptime(str(iDV_START), '%Y%m%d%H%M%S')
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Calculating elapsed time
                try:
                    # Python >=2.7
                    dDV = (oDV_END - oDV_START).total_seconds()

                except:
                    # Python 2.6
                    dDV_END = mktime(oDV_END.timetuple())
                    dDV_START = mktime(oDV_START.timetuple())
                    dDV = dDV_END - dDV_START

                # Calculating time difference between two dates (in days)
                dDt = dDV / 86400
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Calculating gain Kn
                dVarKN = a1dVarKN[0, iIndexDV_START] / (a1dVarKN[0, iIndexDV_START] + np.exp(-dDt / iTimeFilter))
                a1dVarKN[0, iIndexDV_END] = dVarKN

                # Checking if last values in finite or nan
                if a1dVarData_SEL[iIndexDV_END] >= 0:
                    dVarSWI_STEP = (a1dVarSWI_STEP[iIndexDV_START] +
                                    a1dVarKN[0, iIndexDV_END] * (a1dVarData_SEL[iIndexDV_END] -
                                                                a1dVarSWI_STEP[iIndexDV_START]))
                else:
                    dVarSWI_STEP = (a1dVarSWI_STEP[iIndexDV_START] +
                                    a1dVarKN[0, iIndexDV_END] * (-a1dVarSWI_STEP[iIndexDV_START]))

                # Updating SWI values
                a1dVarSWI_STEP[iIndexDV_END] = dVarSWI_STEP
                # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # No data values
            a1dVarSWI_STEP = np.zeros((1, a1dVarDims_SEL[1]))
            a1dVarSWI_STEP[:] = np.nan
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Saving results in SWI
        a2dVarSWI[iP, :] = a1dVarSWI_STEP
        # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Return variable(s)
    return a2dVarSWI
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
