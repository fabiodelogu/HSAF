"""
Library Features:

Name:          Lib_Var_Apps_Geo
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160712'
Version:       '1.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import numpy as np
from Drv_Exception import Exc

# Debug
import matplotlib.pylab as plt
#################################################################################

# --------------------------------------------------------------------------------
# Method to convert decimal degrees to km
def Deg2Km_2(deg, lat=None):
    if lat is None:
        km = deg * 110.54
    else:
        km = deg * 111.32 * np.cos(np.deg2rad(lat))
    return km
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to convert decimal degrees to km (2)
def Deg2Km(deg):
    # Earth radius
    dRE = 6378.1370
    km = deg * (np.pi * dRE) / 180;
    return km
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to convert km to decimal degrees
def Km2Deg(km):
    # Earth radius
    dRE = 6378.1370
    deg = 180 * km / (np.pi * dRE);
    return deg
# --------------------------------------------------------------------------------
