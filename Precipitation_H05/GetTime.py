#-------------------------------------------------------------------------------------
# Class Features
__author__ = 'fabio'
__date__ = '20140415'
__version__ = '1.0.0'
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Library
import time
import datetime
import sys
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Getting date period 
def getDatePeriod(sDateTo, sDateFrom=None, iDateDelta=None, iDateStep=None, iDatePrev = None):
    
    if (sDateFrom and sDateTo) and not iDatePrev:
        oDateFrom = datetime.datetime.strptime(sDateFrom, '%Y%m%d%H%M%S')
        oDateTo = datetime.datetime.strptime(sDateTo, '%Y%m%d%H%M%S')
          
    elif (sDateTo and iDateDelta) and not (sDateFrom or iDatePrev):
        oDateTo = datetime.datetime.strptime(sDateTo, '%Y%m%d%H%M%S')
        oDateFrom = oDateTo - datetime.timedelta(seconds = iDateStep*iDateDelta)
        
    elif (sDateTo and sDateFrom) and (iDatePrev and iDateDelta):
        oDateFrom = datetime.datetime.strptime(sDateFrom, '%Y%m%d%H%M%S')
        oDateTo = datetime.datetime.strptime(sDateTo, '%Y%m%d%H%M%S')
        oDateFrom = oDateTo - datetime.timedelta(seconds = iDateDelta*(iDatePrev + iDateStep))
        
    elif (sDateTo and iDatePrev and iDateDelta) and not sDateFrom:
        oDateTo = datetime.datetime.strptime(sDateTo, '%Y%m%d%H%M%S')
        oDateFrom = oDateTo - datetime.timedelta(days = iDateDelta*(iDatePrev + iDateStep))
        
    #if not iDateStep and iDateDelta:
    #    iDateStep = iDateDelta/iDateDelta

    oDateStep = oDateFrom
    iDateStep = datetime.timedelta(seconds=iDateDelta)

    a1sDatePeriod = []
    while oDateStep <= oDateTo:
        a1sDatePeriod.append(oDateStep.strftime('%Y%m%d%H%M%S'))
        oDateStep += iDateStep
    
    return a1sDatePeriod 
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Class GetTime
class GetTime:

    #-------------------------------------------------------------------------------------
    # Init vars
    iDaysElaborationRange = None
    sTimeRef = None
    sTimeNow = None

    a1sTimeRun = None
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Method time info
    def __init__(self, oSettings=None):

        """
        Function parameters input and output
        :rtype : object
        :param sDateFrom:
        :param sDateTo:
        """
        
        self.iDaysElaborationRange = oSettings.iDaysElaborationRange
        self.sTimeRef = "197001010000"
        self.sTimeNow = oSettings.sTimeNow
        self.iTimeDelta = oSettings.iTimeDelta
        self.sNameProduct = oSettings.oDataSettings['Features']['ProductName']['NameIN']
        
        self.getDateRun()
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------    
    # Getting date now
    def getDateRun(self): 
        
        # Product name definition
        sNameProduct = self.sNameProduct
        # Time delta
        iTimeDeltaSec = self.iTimeDelta
        
        # Checking on datenow format
        if not self.sTimeNow:
            
            # Defined by system
            sTimeNow = time.strftime("%Y%m%d%H%M", time.gmtime())
            oTimeNow = datetime.datetime.strptime(sTimeNow,'%Y%m%d%H%M')
            sYearNow = oTimeNow.strftime('%Y'); sMonthNow = oTimeNow.strftime('%m')
            sDayNow = oTimeNow.strftime('%d'); sHourNow = oTimeNow.strftime('%H')
            
            if (sNameProduct == 'h10'):
                oTimeNow = oTimeNow.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
            elif(sNameProduct == 'h03'):
                oTimeNow = oTimeNow.replace(minute = 0, second = 0, microsecond = 0)
            elif(sNameProduct == 'h05'):
                
                dTimeDeltaHour = float(iTimeDeltaSec/3600); dHourNow = float(sHourNow)
                iHourMod = int(dHourNow%dTimeDeltaHour)
                if(iHourMod == 1):
                    oTimeNow = oTimeNow.replace(hour = int((dHourNow-1)), minute = 0, second = 0, microsecond = 0)
                elif(iHourMod == 2):
                    oTimeNow = oTimeNow.replace(hour = int((dHourNow+1)), minute = 0, second = 0, microsecond = 0)
                else:
                    oTimeNow = oTimeNow.replace(hour = int(dHourNow), minute = 0, second = 0, microsecond = 0)
                
            else:
                sys.exit(' -------> ATTENTION: product name unknown! Check settings file!')
            
            self.sTimeNow = oTimeNow.strftime('%Y%m%d%H%M')
        else:
            
            # Defined by user
            oTimeNow = datetime.datetime.strptime(self.sTimeNow,'%Y%m%d%H%M')
            sYearNow = oTimeNow.strftime('%Y'); sMonthNow = oTimeNow.strftime('%m')
            sDayNow = oTimeNow.strftime('%d'); sHourNow = oTimeNow.strftime('%H')
            
            if (sNameProduct == 'h10'):
                oTimeNow = oTimeNow.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
            elif(sNameProduct == 'h03'):
                oTimeNow = oTimeNow.replace(minute = 0, second = 0, microsecond = 0)
            elif(sNameProduct == 'h05'):
                
                dTimeDeltaHour = float(iTimeDeltaSec/3600); dHourNow = float(sHourNow)
                iHourMod = int(dHourNow%dTimeDeltaHour)
                if(iHourMod == 1):
                    oTimeNow = oTimeNow.replace(hour = int((dHourNow-1)), minute = 0, second = 0, microsecond = 0)
                elif(iHourMod == 2):
                    oTimeNow = oTimeNow.replace(hour = int((dHourNow+1)), minute = 0, second = 0, microsecond = 0)
                else:
                    oTimeNow = oTimeNow.replace(hour = int(dHourNow), minute = 0, second = 0, microsecond = 0)
                
            else:
                sys.exit(' -------> ATTENTION: product name unknown! Check settings file!')
            
            self.sTimeNow = oTimeNow.strftime('%Y%m%d%H%M')
        
        if not self.iDaysElaborationRange:
            self.iDaysElaborationRange = 0;
        
        oTimeFrom = oTimeNow - datetime.timedelta(days = self.iDaysElaborationRange)
        sTimeFrom = oTimeFrom.strftime('%Y%m%d%H%M')
        
        
        self.sTimeTo = oTimeNow.strftime('%Y%m%d%H%M%S')
        self.sTimeFrom = oTimeFrom.strftime('%Y%m%d%H%M%S')
        self.sTimeNow = oTimeNow.strftime('%Y%m%d%H%M%S')
        
        self.a1sTimeRun = getDatePeriod(sDateTo=self.sTimeTo, 
                                        sDateFrom=self.sTimeFrom,
                                        iDateStep=self.iDaysElaborationRange,
                                        iDateDelta=self.iTimeDelta)
        
    #-------------------------------------------------------------------------------------
        



