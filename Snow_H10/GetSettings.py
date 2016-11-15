#-------------------------------------------------------------------------------------
# Class Features
__name__ = 'GetSettings Class'
__author__ = 'fabio'
__date__ = '20140414'
__version__ = '1.0.0'
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Library
import imp
import os
#-------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------
# Class reading settings
class GetSettings:

    #-------------------------------------------------------------------------------------
    # Init vars
    sFileNameRef = None
    sFileNameSatellite = None
    sFileNameOUT = None
    
    sPathDataStatic = None
    sPathDataSatellite = None
    sPathDataDynamicSource = None
    sPathDataDynamicOutcome = None
    sPathTemp = None

    sTimeNow = None
    iDaysElaborationRange = None
    iTempFileDelete = None
    
    iTimeDelta = None
    iTimeBuffer = None
    
    oDataSettings = None
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, sFileName=None):

        #-------------------------------------------------------------------------------------
        # Reading setting file
        """

        :type self: object
        :rtype : object settings
        :param sFileName: file settings in ascii format
        """
        
        oFileSettings = imp.load_source('options', '',  open(sFileName))

        self.sFileNameRef = oFileSettings.sFileNameRef
        #self.sFileNameSatellite = oFileSettings.sFileNameSatellite
        self.sFileNameOUT = oFileSettings.sFileNameOUT
  
        self.sPathDataStatic = oFileSettings.sPathDataStatic
        #self.sPathDataSatellite = oFileSettings.sPathDataSatellite
        self.sPathDataDynamicSource = oFileSettings.sPathDataDynamicSource
        self.sPathDataDynamicOutcome = oFileSettings.sPathDataDynamicOutcome
        #self.sPathDataDB = oFileSettings.sPathDataDB
        self.sPathTemp = oFileSettings.sPathTemp
                
        self.sTimeNow = oFileSettings.sTimeNow
        self.iDaysElaborationRange = oFileSettings.iDaysElaborationRange
        
        self.iTimeDelta = oFileSettings.iTimeDelta
        self.iTimeBuffer = oFileSettings.iTimeBuffer
        
        self.sDomainName = oFileSettings.sDomainName
        
        self.oDataSettings = oFileSettings.oDataSettings
        
        self.iTempFileDelete = oFileSettings.iTempFileDelete

        # Creating temp folder
        if not os.path.exists(oFileSettings.sPathTemp): os.makedirs(oFileSettings.sPathTemp)

        # Creating DB folder
        #if not os.path.exists(oFileSettings.sPathDataDB): os.makedirs(oFileSettings.sPathDataDB)
        
        # Creating data dynamic folder
        if not os.path.exists(oFileSettings.sPathDataDynamicOutcome): os.makedirs(oFileSettings.sPathDataDynamicOutcome)
        #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------





























