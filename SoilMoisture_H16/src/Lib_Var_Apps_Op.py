"""
Library Features:

Name:          Lib_Var_Apps_Op
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160713'
Version:       '1.0.0'
"""

##################################################################################
# Logging
import logging

oLogStream = logging.getLogger('sLogger')

# Global libraries
import numpy as np
from copy import deepcopy

from Drv_Exception import Exc

# Debug
import matplotlib.pylab as plt
##################################################################################

# --------------------------------------------------------------------------------
# Mask variable using a fill value
def maskVarFillValue(a2dVarData, iVarFillValue, oGeoData):

    # Mask finite and nan values
    a2bGeoMaskFinite = oGeoData.a2bGeoDataFinite
    a2bGeoMaskNan = oGeoData.a2bGeoDataNan

    # Mask data using fill value
    a2dVarDataMask = deepcopy(a2dVarData)

    if iVarFillValue:
        a2dVarDataMask = np.where(a2bGeoMaskNan != True, a2dVarDataMask, iVarFillValue)
    else:
        pass

    return a2dVarDataMask
    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
