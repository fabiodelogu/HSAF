"""
Class Features

Name:          GetTime
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160713'
Version:       '3.0.1'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import time, datetime
import numpy as np

import Lib_Time_Apps as Lib_Time_Apps

from Drv_Exception import Exc
######################################################################################

#-------------------------------------------------------------------------------------
# Class time object
class TimeObj(object):
    pass
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Class GetTime
class Time:

    #-------------------------------------------------------------------------------------
    # Variable(s)
    sTimeNow = ''
    oTimeNow = None
    sTimeFrom = ''
    oTimeFrom = None
    sTimeTo = ''
    oTimeTo = None

    a1oTimeSteps = []
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Method time info
    def __init__(self, timenow=time.strftime("%Y%m%d%H%M", time.localtime()), timedelta=3600,
                       timesteppast=0, timestepfut=0, timerefHH=[],
                       timerefworld={'TimeType'	: 'local', 'TimeLoad' : 0, 'TimeSave' : 0}):
        
        # Store information in global workspace
        self.sTimeNow = timenow
        self.iTimeDelta = timedelta
        self.iTimeStepPast = timesteppast
        self.iTimeStepFuture = timestepfut
        self.sTimeHHRef = timerefHH
        self.oTimeWorldRef = timerefworld

    #-------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to get time information
    def getTime(self):

        # Set time now
        self.__setTimeNow()
        # Set time ref for hours tags
        self.__setTimeHHRef()
        # Set time from, time to and time steps
        self.__setTimes()
        # Print information about times
        self.__printTimes()

        # Method to select output data
        oTime = self.__selectInfo()

        return oTime

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to select time information
    def __selectInfo(self):

        oTime = TimeObj()
        for sVarName in vars(self):

            oVarName = getattr(self, sVarName)
            setattr(oTime, sVarName, oVarName)

        return oTime

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to print information about times
    def __printTimes(self):

        # Info times
        oLogStream.info(' ----> Defining TimeNow: ' + str(self.sTimeNow))
        oLogStream.info(' ----> Defining TimeFrom: ' + str(self.sTimeFrom))
        oLogStream.info(' ----> Defining TimeTo: ' + str(self.sTimeTo))

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to set time now
    def __setTimeNow(self):
        [self.sTimeNow, sTimeNowFormat] = Lib_Time_Apps.getTimeNow(self.sTimeNow, self.oTimeWorldRef['TimeType'])
        self.oTimeNow = datetime.datetime.strptime(self.sTimeNow, sTimeNowFormat)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to set time reference hh
    def __setTimeHHRef(self):

        # Select time format (using time now string)
        sTimeFormat = Lib_Time_Apps.defineTimeFormat(self.sTimeNow)

        # Check if HH time reference is defined
        if not self.sTimeHHRef:
            oTimeNow = datetime.datetime.strptime(self.sTimeNow, sTimeFormat)
            oTimeNow = oTimeNow.replace(minute=0, second=0, microsecond=0)
        else:
            oTimeNow = datetime.datetime.strptime(self.sTimeNow, sTimeFormat)

            a1iTimeDiff = np.zeros([len(self.sTimeHHRef), 1])
            a1iTimeDiff[:] = np.nan;
            for iHH, sHH in enumerate(self.sTimeHHRef):
                oTimeRef = oTimeNow.replace(hour=int(sHH), minute=0, second=0, microsecond=0)
                oTimeDiff = oTimeNow - oTimeRef
                
                try:
                    # Python >=2.7
                    iTimeDiff = oTimeDiff.total_seconds()
                except:
                    # Python 2.6
                    iTimeNow = time.mktime(oTimeNow.timetuple());
                    iTimeRef = time.mktime(oTimeRef.timetuple());
                    iTimeDiff = iTimeNow - iTimeRef

                if iTimeDiff >= 0:
                    a1iTimeDiff[iHH] = iTimeDiff;
                else:
                    pass

            # Check if all result(s) are nan(s) --> select one day before
            if np.all(np.isnan(a1iTimeDiff)):

                Exc.getExc(
                    ' -----> WARNING: TimeHHRef generates TimeRef greater then TimeNow! Selecting TimeNow and TimeRef one day before!',
                    2, 1)
                oTimeRef = oTimeRef - datetime.timedelta(seconds=86400)
                oTimeNow = oTimeNow - datetime.timedelta(seconds=86400)
                oTimeDiff = oTimeNow - oTimeRef;

                try:
                    # Python >=2.7
                    iTimeDiff = oTimeDiff.total_seconds()
                except:
                    # Python 2.6
                    iTimeNow = time.mktime(oTimeNow.timetuple());
                    iTimeRef = time.mktime(oTimeRef.timetuple());
                    iTimeDiff = iTimeNow - iTimeRef

                a1iTimeDiff[iHH] = iTimeDiff;
            else:
                pass

            # Select time now and time HH ref
            iTimeDiffIndex = np.argmin(np.where(np.isfinite(a1iTimeDiff)))
            sTimeHHRef = self.sTimeHHRef[iTimeDiffIndex]
            # Select time now
            oTimeNow = oTimeNow.replace(hour=int(sTimeHHRef), minute=0, second=0, microsecond=0)

        # Update time now
        self.sTimeNow = oTimeNow.strftime(sTimeFormat)
        self.sTimeHHRef = sTimeHHRef

        self.oTimeNow = datetime.datetime.strptime(self.sTimeNow, sTimeFormat)

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to set times and time steps
    def __setTimes(self):

        # Get and check TimeFrom and sTimeTo
        [self.sTimeFrom, sTimeFromFormat] = Lib_Time_Apps.getTimeFrom(self.sTimeNow, self.iTimeDelta, self.iTimeStepPast)
        self.oTimeFrom = datetime.datetime.strptime(self.sTimeFrom, sTimeFromFormat)
        [self.sTimeTo, sTimeToFormat] = Lib_Time_Apps.getTimeTo(self.sTimeNow, self.iTimeDelta, self.iTimeStepFuture)
        self.oTimeTo = datetime.datetime.strptime(self.sTimeTo, sTimeToFormat)

        # Get TimeSteps
        self.a1oTimeSteps = Lib_Time_Apps.getTimeSteps(self.sTimeFrom, self.sTimeTo, self.iTimeDelta)

    # -------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------

