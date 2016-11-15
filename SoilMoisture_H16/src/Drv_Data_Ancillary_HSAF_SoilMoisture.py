"""
Class Features

Name:          Drv_Data_Ancillary
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160708'
Version:       '1.0.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Libraries
import datetime

from numpy import zeros, argmin

from os.path import isfile, join, split

from src.Lib_Op_System_Apps import selectFileName, createFileNamePattern, getFileNameRegExp
from src.Lib_Op_Dict_Apps import prepareDictKey, lookupDictKey
from src.Drv_Exception import Exc
from src.Lib_Op_String_Apps import defineString
from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_File_Zip import Drv_File_Zip
from src.Lib_Time_Apps import getTimeNow, findTimeDiff

# Debug
# import matplotlib.pylab as plt
######################################################################################

# -------------------------------------------------------------------------------------
# Selected data dictionary
oDictGet = {'SWI_Statistics': dict(Longitude='Longitude', Latitude='Latitude',
                                   SWI_Max_T06='SWI_Max_T06',
                                   SWI_Min_T06='SWI_Min_T06',
                                   SWI_StDev_T06='SWI_StDev_T06',
                                   SWI_Mean_T06='SWI_Mean_T06',
                                   SWI_Max_T12='SWI_Max_T12',
                                   SWI_Min_T12='SWI_Min_T12',
                                   SWI_StDev_T12='SWI_StDev_T12',
                                   SWI_Mean_T12='SWI_Mean_T12',
                                   SWI_Max_T32='SWI_Max_T32',
                                   SWI_Min_T32='SWI_Min_T32',
                                   SWI_StDev_T32='SWI_StDev_T32',
                                   SWI_Mean_T32='SWI_Mean_T32',
                                   ),
            'SM_Statistics': dict(Longitude='Longitude', Latitude='Latitude',
                                  SM_Max_Layer1='SM_Max_Layer1',
                                  SM_Min_Layer1='SM_Min_Layer1',
                                  SM_StDev_Layer1='SM_StDev_Layer1',
                                  SM_Mean_Layer1='SM_Mean_Layer1',
                                  SM_Max_Layer2='SM_Max_Layer2',
                                  SM_Min_Layer2='SM_Min_Layer2',
                                  SM_StDev_Layer2='SM_StDev_Layer2',
                                  SM_Mean_Layer2='SM_Mean_Layer2',
                                  SM_Max_Layer3='SM_Max_Layer3',
                                  SM_Min_Layer3='SM_Min_Layer3',
                                  SM_StDev_Layer3='SM_StDev_Layer3',
                                  SM_Mean_Layer3='SM_Mean_Layer3',
                                  ),
            }


# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Class data object
class DataObj(object):
    pass

# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Class DataAncillary
class DataAncillary:

    # -------------------------------------------------------------------------------------
    # Class variable(s)
    oFileData = None
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Initialize class
    def __init__(self, sFileName=None, sDataName=None, oDataObject=None, sTimeNow=''):

        # Pass variable to global class
        self.__sFileName = sFileName
        self.__sDataName = sDataName
        self.__oDataObject = oDataObject
        self.__sTimeNow = sTimeNow

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to get data
    def getData(self):

        # Get time now
        self.__getTime()

        # Get filename based on time now
        self.__getFile()

        # Select method to define geographical information
        if isfile(self.__sFileName):
            self.__readData()
        else:
            Exc.getExc(' -----> ERROR: filename is undefined! (' + self.__sFileName + ')', 1, 1)

        # Method to check name between data selected dictionary and dataset input name
        self.__checkName()

        # Method to set variable name of data
        self.__setName()

        # Method to add data to an existing geographical object
        self.__addGrid()

        # Method to select output dictionary
        self.__selectDict()

        # Method to select output data
        oData = self.__selectInfo()

        return oData

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to get time now
    def __getTime(self):

        if self.__sTimeNow == '':
            [sTimeNow, sFormatNow] = getTimeNow()
            oTimeNow = datetime.datetime.strptime(sTimeNow, sFormatNow)
            oTimeNow = oTimeNow.replace(hour=0, minute=0, second=0, microsecond=0)
            sTimeNow = oTimeNow.strftime(sFormatNow)

            self.__sTimeNow = sTimeNow
        else:
            pass

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to get filename based on time
    def __getFile(self):

        sFileName = self.__sFileName
        sTimeNow = self.__sTimeNow
        sFileTimeFormat = '$yyyy$mm$dd$HH$MM'

        [sFilePath, sFileName] = split(sFileName)

        sFilePattern = createFileNamePattern(sFileName, {sFileTimeFormat: '*[0-9]'})
        a1oFileName = selectFileName(sFilePath, sFilePattern)
        a1oFileTime = getFileNameRegExp(a1oFileName)

        a1iTimeDiff = zeros([len(a1oFileTime), 1])
        for iFileTime, sFileTime in enumerate(a1oFileTime):
            iTimeDiff = findTimeDiff(sTimeNow, sFileTime)
            a1iTimeDiff[iFileTime] = iTimeDiff

        sFileTime_SELECT = a1oFileTime[argmin(a1iTimeDiff)]
        sFileName_SELECT = defineString(sFileName, {sFileTimeFormat: sFileTime_SELECT})

        self.__sFileName = join(sFilePath, sFileName_SELECT)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to check key in data selected dictionary
    def __checkName(self):
        if oDictGet:
            if self.__sDataName in oDictGet:
                pass
            else:
                Exc.getExc(' -----> WARNING: dataset name mismatch! (' + self.__sDataName + ')', 2, 1)
        else:
            pass

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to select dictionary data
    def __selectDict(self):

        if oDictGet:
            sDataName = self.__sDataName
            oDataSet = getattr(self, sDataName)
            if sDataName in oDictGet:
                oDictSet = oDictGet[sDataName]
                if oDataSet:
                    oDictSel = {}
                    for sKey, sValue in oDictSet.iteritems():
                        oDictKeys = prepareDictKey(sValue, '/')
                        if oDictKeys:
                            oDictSel[sKey] = lookupDictKey(oDataSet, *oDictKeys)
                        else:
                            pass
                    setattr(self, sDataName, oDictSel)
                else:
                    pass
            else:
                pass
        else:
            pass

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to select data information
    def __selectInfo(self):

        oData = DataObj()
        for sVarName in vars(self):
            if not sVarName.startswith('_'):
                oVarName = getattr(self, sVarName)
                if oVarName:
                    setattr(oData, sVarName, oVarName)
                else:
                    pass
            else:
                pass

        return oData

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to read data
    def __readData(self):

        # -------------------------------------------------------------------------------------
        # Test if file ancillary is zipped or unzipped
        try:
            # Unzip file
            oZipDrv = Drv_File_Zip(self.__sFileName, 'u', None, '.gz').oFileWorkspace
            [oFile_IN, oFile_OUT] = oZipDrv.oFileLibrary.openZip(oZipDrv.sFileName_IN,
                                                                 oZipDrv.sFileName_OUT,
                                                                 oZipDrv.sZipMode)

            oZipDrv.oFileLibrary.unzipFile(oFile_IN, oFile_OUT)
            oZipDrv.oFileLibrary.closeZip(oFile_IN, oFile_OUT)

            # Open file after unzipping
            oFileDriver = Drv_Data_IO(oZipDrv.sFileName_OUT, 'r').oFileWorkspace
            oFileHandle = oFileDriver.oFileLibrary.openFile(join(oFileDriver.sFilePath, oFileDriver.sFileName),
                                                            oFileDriver.sFileMode)

        except:

            # Read data file unzipped
            oFileDriver = Drv_Data_IO(self.__sFileName, 'r').oFileWorkspace
            oFileHandle = oFileDriver.oFileLibrary.openFile(join(oFileDriver.sFilePath, oFileDriver.sFileName),
                                                            oFileDriver.sFileMode)
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get data (all variable(s))
        oFileData = oFileDriver.oFileLibrary.getVars(oFileHandle)
        oFileDriver.oFileLibrary.closeFile(oFileHandle)

        # Return data
        self.oFileData = oFileData
        # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to add data to existence geographical object
    def __addGrid(self):

        if self.__oDataObject:

            # Get domain reference
            oData_REF = self.__oDataObject

            if not hasattr(oData_REF, self.__sDataName):

                # Set data into domain reference
                oData_ADD = getattr(self, self.__sDataName)
                setattr(oData_REF, self.__sDataName, oData_ADD)

                for sVarName in vars(oData_REF):
                    oVarName = getattr(oData_REF, sVarName)
                    setattr(self, sVarName, oVarName)

            else:
                pass
        else:
            pass

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to set specified data name
    def __setName(self):

        from copy import deepcopy

        if not hasattr(self, self.__sDataName):

            # Set dictionary name and delete old general copy
            setattr(self, self.__sDataName, deepcopy(self.oFileData))
            self.oFileData.clear()

        else:
            pass
            # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
