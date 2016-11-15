"""
Library Features:

Name:          Lib_Op_String_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160704'
Version:       '2.0.0'
"""

#######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

from Drv_Exception import Exc

# Debug
# import matplotlib.pylab as plt
#######################################################################################


# -------------------------------------------------------------------------------------
# Method to define string
def defineString(sString='', oDictTags=None):

    if sString != '':
        if not oDictTags:
            pass
        elif oDictTags:
            for sKey, oValue in oDictTags.items():
                if isinstance(oValue, basestring):
                    sString = sString.replace(sKey, oValue)
                elif isinstance(oValue, int):
                    sString = sString.replace(sKey, str(int(oValue)))
                elif isinstance(oValue, float):
                    sString = sString.replace(sKey, str(float(oValue)))
                else:
                    sString = sString.replace(sKey, str(oValue))
    else:
        pass

    return sString
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to convert UNICODE to ASCII
def convertUnicode2ASCII(sStringUnicode, convert_option='ignore'):
    # convert_option "ignore" or "replace"
    sStringASCII = sStringUnicode.encode('ascii', convert_option)
    return sStringASCII
# -------------------------------------------------------------------------------------
