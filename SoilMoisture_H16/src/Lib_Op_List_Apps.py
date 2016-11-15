"""
Library Features:

Name:          Lib_Op_List_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20161011'
Version:       '1.0.0'
"""

#######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

#from Drv_Exception import Exc

# Debug
# import matplotlib.pylab as plt
#######################################################################################

# -------------------------------------------------------------------------------------
# Method to check if list element(s) are all the same
def checkListAllSame(items=False):
    if items:
        items_check = all(x == items[0] for x in items)
    else:
        items_check = False
    return items_check
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to get list unique value(s)
def getListUnique(oList=None):

    if oList:
        oSet = set(oList)
        oListUnique = list(oSet)
    else:
        oListUnique = None

    return oListUnique
# -------------------------------------------------------------------------------------
