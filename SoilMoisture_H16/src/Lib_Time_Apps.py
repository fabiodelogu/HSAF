"""
Library Features:

Name:          Lib_Time_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160623'
Version:       '1.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import time
import datetime
from time import mktime
from numpy import abs

from Drv_Exception import Exc

# Debug
# import matplotlib.pylab as plt
#################################################################################

# --------------------------------------------------------------------------------
# Method to check time format
def correctTimeLength(sTime):
    if len(sTime) == 12:

        sTimeUpd = sTime

    elif len(sTime) >= 8 and len(sTime) < 12:

        iTimeLength = len(sTime)

        iTimeLessDigits = 12 - iTimeLength
        sTimeLessFormat = '0' * iTimeLessDigits
        sTimeUpd = sTime + sTimeLessFormat

    elif len(sTime) > 12:
        Exc.getExc(' -----> ERROR: sTime has not allowed length (greater then 12 char). sTime cannot defined!', 1, 1)
    elif len(sTime) < 8:
        Exc.getExc(' -----> ERROR: sTime has not allowed length (less then 8 char). sTime cannot defined!', 1, 1)

    sTimeUpdFormat = defineTimeFormat(sTimeUpd)

    # Check time format definition
    checkTimeFormat(sTimeUpd, sTimeUpdFormat)

    return sTimeUpd, sTimeUpdFormat
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to check time format for time string
def checkTimeFormat(sTime, sTimeFormat='%Y%m%d%H%M'):
    try:
        datetime.datetime.strptime(sTime, sTimeFormat)
    except:
        Exc.getExc(' -----> ERROR: sTime has not correct format. sTime cannot defined!', 1, 1)
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define time format
def defineTimeFormat(sTime):
    sTimeFormat = ''
    if len(sTime) == 12:
        sTimeFormat = '%Y%m%d%H%M'
    elif len(sTime) == 10:
        sTimeFormat = '%Y%m%d%H'
    elif len(sTime) == 8:
        sTimeFormat = '%Y%m%d'
    else:
        Exc.getExc(' -----> ERROR: sTime has not allowed length. sTimeFormat cannot defined!', 1, 1)

    return sTimeFormat
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to convert local time to GMT time and viceversa (sTimeLocal  --> 'yyyymmddHHMM')
def convertTimeLOCxGMT(sTime_IN=None, iTimeDiff=0):
    if sTime_IN:
        sTimeFormat_IN = defineTimeFormat(sTime_IN)
        sTimeFormat_OUT = sTimeFormat_IN

        oTime_IN = datetime.datetime.strptime(sTime_IN, sTimeFormat_IN)
        oTime_IN = oTime_IN.replace(minute=0, second=0, microsecond=0)
        oTime_OUT = oTime_IN + datetime.timedelta(seconds=iTimeDiff * 3600)
        sTime_OUT = oTime_OUT.strftime(sTimeFormat_OUT)
    else:
        Exc.getExc(" -----> ERROR: sTime_IN not defined! sTime_OUT cannot calculated!", 1, 1)

    return sTime_OUT
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to get local time
def getTimeLocal():
    sTimeFormat = "%Y%m%d%H%M"
    return time.strftime(sTimeFormat, time.localtime())  # ---> LOCAL TIME
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to get GMT time
def getTimeGMT():
    sTimeFormat = "%Y%m%d%H%M"
    return time.strftime(sTimeFormat, time.gmtime())  # ---> GMT TIME
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define sTimeNow
def getTimeNow(sTimeNow='', sTimeRefType='local'):
    if not sTimeNow == '':
        [sTimeNow, sTimeFormat] = correctTimeLength(sTimeNow)
    elif sTimeNow == '':

        if sTimeRefType == 'local':
            sTimeNow = getTimeLocal()
        elif sTimeRefType == 'GMT':
            sTimeNow = getTimeGMT()
        else:
            Exc.getExc(' -----> WARNING: sTimeTypeRef is not defined correctly! sTimeNow initilized as local time!',
                         2, 1)
            sTimeNow = getTimeLocal()

        [sTimeNow, sTimeFormat] = correctTimeLength(sTimeNow)

    else:
        Exc.getExc(' -----> ERROR: sTimeNow format is unknown. Please check your time string!', 1, 1)

    return sTimeNow, sTimeFormat
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define sTimeTo
def getTimeTo(sTimeFrom=None, iTimeDelta=3600, iTimeStep=0):
    if sTimeFrom:
        sTimeFormat = defineTimeFormat(sTimeFrom)
        oTimeFrom = datetime.datetime.strptime(sTimeFrom, sTimeFormat)
        oTimeTo = oTimeFrom + datetime.timedelta(seconds=iTimeStep * iTimeDelta)
        sTimeTo = oTimeTo.strftime(sTimeFormat)
    else:
        Exc.getExc(" -----> ERROR: sTimeFrom not defined! sTimeTo cannot calculated!", 1, 1)

    return sTimeTo, sTimeFormat
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define sTimeFrom
def getTimeFrom(sTimeTo=None, iTimeDelta=3600, iTimeStep=0):
    if sTimeTo:
        sTimeFormat = defineTimeFormat(sTimeTo)
        oTimeTo = datetime.datetime.strptime(sTimeTo, sTimeFormat)
        oTimeFrom = oTimeTo - datetime.timedelta(seconds=iTimeStep * iTimeDelta)
        sTimeFrom = oTimeFrom.strftime(sTimeFormat)
    else:
        Exc.getExc(" -----> ERROR: sTimeTo not defined! sTimeFrom cannot calculated!", 1, 1)

    return sTimeFrom, sTimeFormat
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define a1oTimeSteps (using sTimeFrom, sTimeTo, iTimeDelta, iTimeStep)
def getTimeSteps(sTimeFrom=None, sTimeTo=None, iTimeDelta=3600, iTimeStep=0):
    # Case sTimeFrom and sTimeTo to define a1oTimeSteps
    if sTimeFrom and sTimeTo and iTimeDelta:

        sTimeFromFormat = defineTimeFormat(sTimeFrom)
        sTimeToFormat = defineTimeFormat(sTimeTo)

        oTimeFrom = datetime.datetime.strptime(sTimeFrom, sTimeFromFormat)
        oTimeTo = datetime.datetime.strptime(sTimeTo, sTimeToFormat)

    elif sTimeFrom and iTimeDelta and iTimeStep:

        sTimeTo = getTimeTo(sTimeFrom, iTimeDelta, iTimeStep)

        sTimeFromFormat = defineTimeFormat(sTimeFrom)
        sTimeToFormat = defineTimeFormat(sTimeTo)

        oTimeFrom = datetime.datetime.strptime(sTimeFrom, sTimeFromFormat)
        oTimeTo = datetime.datetime.strptime(sTimeTo, sTimeToFormat)

    elif sTimeTo and iTimeDelta and iTimeStep:

        sTimeFrom = getTimeFrom(sTimeTo, iTimeDelta, iTimeStep)

        sTimeFromFormat = defineTimeFormat(sTimeFrom)
        sTimeToFormat = defineTimeFormat(sTimeTo)

        oTimeFrom = datetime.datetime.strptime(sTimeFrom, sTimeFromFormat)
        oTimeTo = datetime.datetime.strptime(sTimeTo, sTimeToFormat)

    # Define a1oTimeSteps
    oTimeStep = oTimeFrom
    iTimeDelta = datetime.timedelta(seconds=iTimeDelta)

    a1oTimeSteps = []
    while oTimeStep <= oTimeTo:
        a1oTimeSteps.append(oTimeStep.strftime(sTimeToFormat))
        oTimeStep += iTimeDelta

    return a1oTimeSteps

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to check max time interval
def checkTimeMaxInt(a1oTime_Max=None, a1oTime_Test=None):

    if a1oTime_Test:
        if a1oTime_Max:

            sTime_From_Max = a1oTime_Max[0]
            sFormat_From_Max = defineTimeFormat(sTime_From_Max)
            oTime_From_Max = datetime.datetime.strptime(sTime_From_Max, sFormat_From_Max)
            sTime_To_Max = a1oTime_Max[-1]
            sFormat_To_Max = defineTimeFormat(sTime_To_Max)
            oTime_To_Max = datetime.datetime.strptime(sTime_To_Max, sFormat_To_Max)
            sTime_From_Test = a1oTime_Test[0]
            sFormat_From_Test = defineTimeFormat(sTime_From_Test)
            oTime_From_Test = datetime.datetime.strptime(sTime_From_Test, sFormat_From_Test)
            sTime_To_Test = a1oTime_Test[-1]
            sFormat_To_Test = defineTimeFormat(sTime_To_Test)
            oTime_To_Test = datetime.datetime.strptime(sTime_To_Test, sFormat_To_Test)

            if oTime_From_Max >= oTime_From_Test:
                oTime_From_Upd = oTime_From_Max
                sTime_From_Upd = oTime_From_Upd.strftime(sFormat_From_Max)
            else:
                oTime_From_Upd = oTime_From_Test
                sTime_From_Upd = oTime_From_Upd.strftime(sFormat_From_Test)

            if oTime_To_Max >= oTime_To_Test:
                oTime_To_Upd = oTime_To_Max
                sTime_To_Upd = oTime_To_Upd.strftime(sFormat_To_Max)
            else:
                oTime_To_Upd = oTime_To_Test
                sTime_To_Upd = oTime_To_Upd.strftime(sFormat_From_Test)

        else:
            sTime_From_Upd = a1oTime_Test[0]
            sTime_To_Upd = a1oTime_Test[-1]
    else:
        sTime_From_Upd = None
        sTime_To_Upd = None

    return sTime_From_Upd, sTime_To_Upd

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to find difference between time and a list of times
def findTimeDiff(sTimeCheck, sTimeTest):

    sTimeCheckFormat = defineTimeFormat(sTimeCheck)
    oTimeCheck = datetime.datetime.strptime(sTimeCheck, sTimeCheckFormat)

    sTimeTestFormat = defineTimeFormat(sTimeTest)
    oTimeTest = datetime.datetime.strptime(sTimeTest, sTimeTestFormat)

    # Calculating elapsed time
    try:
        # Python >=2.7
        dDV = (oTimeCheck - oTimeTest).total_seconds()

    except:
        # Python 2.6
        dDV_END = mktime(oTimeTest.timetuple())
        dDV_START = mktime(oTimeCheck.timetuple())
        dDV = dDV_END - dDV_START

    return abs(dDV)
# --------------------------------------------------------------------------------

