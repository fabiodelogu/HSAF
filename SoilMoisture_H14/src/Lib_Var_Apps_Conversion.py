"""
Library Features:

Name:          Lib_Var_Apps_Conversion
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160713'
Version:       '1.6.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
import numpy as np

from Drv_Exception import Exc

# Debug
#import matplotlib.pylab as plt
#################################################################################

#--------------------------------------------------------------------------------
# Method to compute air pressure [kPa] starting from [hPa]
def computeVarhPAtokPA(a2dVar_IN):
    # Compute ending variable values
    a2dVar_OUT = a2dVar_IN / 10
    return a2dVar_OUT
#--------------------------------------------------------------------------------
    
#--------------------------------------------------------------------------------
# Method to compute net short-wave radiation [W/m^2] to incoming short-wave [W/m^2]
def computeVarNetSWtoIncSW(a2dVar_IN, dAlbedo=0.23):
    # Compute ending variable values
    a2dVar_OUT = a2dVar_IN / (1 - dAlbedo)
    return a2dVar_OUT
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to compute rain [mm] starting from [m]
def computeVarMtoMM(a2dVar_IN):
    # Compute ending variable values
    a2dVar_OUT = a2dVar_IN * 1000.0
    return a2dVar_OUT
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to compute temperature [C] starting from [K]
def computeVarKtoC(a2dVar_IN):
    # Compute ending variable values
    a2dVar_OUT = a2dVar_IN - 273.15
    return a2dVar_OUT
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to compute wind speed using u and v components
def computeVarUVtoSpeed(a2dVar_IN_1, a2dVar_IN_2):
    # Compute ending variable values
    a2dVar_OUT = np.sqrt(a2dVar_IN_1**2 + a2dVar_IN_2**2)
    return a2dVar_OUT
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to compute from [-] to [%]
def computeVarINDtoPERC(a2dVar_IN, dVarMax_OUT=np.nan, dVarMin_OUT=np.nan):
    # Compute ending variable values
    a2dVar_OUT = a2dVar_IN * 100.0
    # Variable limits (just in case)
    a2dVar_OUT[a2dVar_OUT >= 100.0] = dVarMax_OUT
    a2dVar_OUT[a2dVar_OUT <= 0.0] = dVarMin_OUT
    return a2dVar_OUT
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to compute from [%] to [-]
def computeVarPERCtoIND(a2dVar_IN, dVarMax_OUT=np.nan, dVarMin_OUT=np.nan):
    # Compute ending variable values
    a2dVar_OUT = a2dVar_IN / 100.0
    # Variable limits (just in case)
    a2dVar_OUT[a2dVar_OUT >= 1.0] = dVarMax_OUT
    a2dVar_OUT[a2dVar_OUT <= 0.0] = dVarMin_OUT
    return a2dVar_OUT
#--------------------------------------------------------------------------------
