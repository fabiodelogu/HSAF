"""
Class Features

Name:          Cpl_Apps_Satellite_DynamicData_HSAF_SWI_H16_Raw
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20161010'
Version:       '4.0.1'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os
import glob
import numpy as np

from os.path import join, split

import src.Lib_Analysis_Interpolation as Lib_Analysis

from src.Drv_Analysis_Interpolation import Drv_Analysis as Drv_Analysis

import src.Lib_Time_Apps as Lib_Time_Apps

from src.Drv_Exception import Exc
from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_File_Zip import Drv_File_Zip

from src.Lib_File_Zip_Apps import removeFileUnzip, removeFileZip, addFileExtZip

from src.Lib_Op_System_Apps import deleteFileName, defineFileName, checkFileName, defineFolder
from src.Lib_Op_String_Apps import defineString
from src.Lib_File_Log_Apps import getFileHistory, writeFileHistory, checkSavingTime
from src.Lib_Op_Dict_Apps import prepareDictKey, lookupDictKey, removeDictKeys

from src.Lib_Analysis_Computation_HSAF_SoilMoisture import computeVarSWI

# Debug
#import matplotlib.pylab as plt
######################################################################################

# -------------------------------------------------------------------------------------
# Class
class Cpl_Apps_Satellite_DynamicData_HSAF_SWI_H16_Raw:
    # -------------------------------------------------------------------------------------
    # Class variable(s)
    oTags = None
    bData_SOURCE = True

    a1oFileDataDyn_CHK = None

    a1oFileDataDyn_SOURCE = None
    a1oVarsInfoDyn_SOURCE = None

    a1oFileDataDyn_GET = None
    a1oFileDataGeo_GET = None

    a1oFileDataDyn_PAR = None
    a1oFileTimeDyn_PAR = None

    a1oFileDataDyn_CMP = None
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTime=None, oDataGeo=None, oDataInfo=None):

        # Data settings and data reference
        self.oDataTime = oDataTime
        self.oDataGeo = oDataGeo
        self.oDataInfo = oDataInfo

        self.sPathClass = os.getcwd()
        self.sPathSrc = join(os.getcwd(), 'src')

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to define run tags
    def defineDynamicTags(self, sTime):

        # Get time information
        sTime_TAG = sTime
        # Get other information
        sDomainName = self.oDataInfo.oInfoSettings.oParamsInfo['DomainName']

        # Create tags dictionary
        oTagsDict = {'$yyyy': sTime_TAG[0:4],
                     '$mm': sTime_TAG[4:6], '$dd': sTime_TAG[6:8], '$HH': sTime_TAG[8:10],
                     '$MM': sTime_TAG[10:12], '$DOMAIN': sDomainName}

        self.oTags = oTagsDict

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to check data availability
    def checkDynamicData(self, sTime):

        # -------------------------------------------------------------------------------------
        # Info
        os.chdir(self.sPathSrc)
        sTime_CHK = sTime
        oLogStream.info(' ====> CHECK DATA AT TIME: ' + sTime_CHK + ' ... ')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get path information
        sPathCache_CHK = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        sPathCache_CHK = defineFolder(sPathCache_CHK, self.oTags)

        sPathDataDyn_CHK = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicOutcome']
        sPathDataDyn_CHK = defineFolder(sPathDataDyn_CHK, self.oTags)

        # Get outcome variable information
        oVarsWorkspace_CHK = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic

        # Get time information
        iTimeStep_CHK = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeStep'])
        iTimeUpd_CHK = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeUpd'])
        a1oTimeSteps_CHK = self.oDataTime.a1oTimeSteps
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Condition to save file for reanalysis period
        bSaveTime_CHK = checkSavingTime(sTime_CHK, a1oTimeSteps_CHK, iTimeStep_CHK, iTimeUpd_CHK)
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Cycle(s) on file type
        a1sFileName_CHK = []
        a1bFileName_CHK = []
        a1sFileTime_CHK = []
        a1oFileDataDyn_CHK = {}
        for sFileType in oVarsWorkspace_CHK:

            # -------------------------------------------------------------------------------------
            # Check file type
            if sFileType == 'NetCDF':

                # Check file
                sFileCache_CHK = os.path.join(sPathCache_CHK, 'Satellite_HSAF-SWI-H16-RAW_FILENC_' + sTime_CHK + '.history')
                bFileCache_CHK = os.path.isfile(sFileCache_CHK)

                # Check file status
                if bFileCache_CHK is True:
                    a1sFileName_CHK = getFileHistory(sFileCache_CHK)

                    for sFileName_CHK in a1sFileName_CHK[0]:

                        bFileName_CHK = os.path.isfile(sFileName_CHK)

                        if bFileName_CHK is True:

                            if bSaveTime_CHK is True:
                                a1bFileName_CHK.append(False)
                                a1sFileName_CHK.append(None)
                                a1sFileTime_CHK.append(sTime_CHK)
                                deleteFileName(sFileName_CHK)

                            else:
                                a1bFileName_CHK.append(True)
                                a1sFileName_CHK.append(sFileName_CHK)
                                a1sFileTime_CHK.append(sTime_CHK)
                        else:
                            a1bFileName_CHK.append(False)
                            a1sFileName_CHK.append(None)
                            a1sFileTime_CHK.append(sTime_CHK)
                            deleteFileName(sFileName_CHK)

                else:
                    a1bFileName_CHK.append(False)
                    a1sFileName_CHK.append(None)
                    a1sFileTime_CHK.append(sTime_CHK)

            else:
                pass

            ### Debug ###
            # a1bFileName_CHK = []; a1bFileName_CHK.append(True)
            ### Debug ###

            # Saving results of checking file 
            a1oFileDataDyn_CHK = zip(a1sFileTime_CHK, a1sFileName_CHK, a1bFileName_CHK)
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Return check status 
        oLogStream.info(' ====> CHECK DATA AT TIME: ' + sTime + ' ... OK')
        # Return variable(s)
        self.a1oFileDataDyn_CHK = a1oFileDataDyn_CHK
        # ------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to retrieve data 
    def retrieveDynamicData(self, sTime):

        # -------------------------------------------------------------------------------------
        # Start message
        os.chdir(self.sPathSrc)
        sTime_RET = sTime
        oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... ')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get path information
        sPathDataDyn_SOURCE = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        # Get IN variable information
        oVarWorkspace_IN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        # Get check history 
        a1oFileDataDyn_CHK = self.a1oFileDataDyn_CHK
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check time steps selection
        if a1oFileDataDyn_CHK:

            # -------------------------------------------------------------------------------------
            # Checking time step data processing
            oTimeMatch = [iS for iS in a1oFileDataDyn_CHK if sTime_RET in iS]
            a1oTimeMatch = zip(*oTimeMatch)
            if a1oTimeMatch[2][0] is False:

                # -------------------------------------------------------------------------------------
                # Cycle(s) on file type(s)
                a1oFileDataDyn_SOURCE = {}
                a1oVarsInfoDyn_SOURCE = {}
                for sFileType in oVarWorkspace_IN:

                    # Get variable(s) information
                    oVarsInfo_IN = oVarWorkspace_IN[sFileType]

                    # Cycle(s) on variable(s)
                    for sVarType in oVarsInfo_IN:

                        # Get var information
                        oVarInfo_IN = oVarsInfo_IN[sVarType]

                        # Compute day steps using var time step
                        iVarTimeStep_IN = oVarInfo_IN['VarTimeStep']
                        iVarDayStep_IN = 86400/iVarTimeStep_IN

                        # Get variable(s) component(s)
                        sVarFunc_IN_LOAD = oVarInfo_IN['VarOp']['Op_Load']['Func']
                        oVarName_IN_LOADIN = oVarInfo_IN['VarOp']['Op_Load']['Comp']['IN']
                        oVarName_IN_LOADOUT = oVarInfo_IN['VarOp']['Op_Load']['Comp']['OUT']

                        oVarName_IN_MissValue = oVarInfo_IN['VarOp']['Op_Load']['Missing_value']
                        oVarName_IN_ValidRng = oVarInfo_IN['VarOp']['Op_Load']['Valid_range']
                        sVarName_IN_Zip = oVarInfo_IN['VarOp']['Op_Load']['Zip']

                        oVarMethodInterp_IN = oVarInfo_IN['VarOp']['Op_Math']['Interpolation']
                        oVarMethodAggreg_IN = oVarInfo_IN['VarOp']['Op_Math']['Aggregation']

                        # Get generic filename
                        sFileDataDyn_RAW = oVarInfo_IN['VarSource']

                        # File time period definition
                        iTimeDataDyn_IN = int(oVarInfo_IN['VarTimeStep'])

                        # Get days period max to be considered (over all variable(s) components)
                        a1iVarDays_IN_LOADOUT = np.zeros([len(oVarName_IN_LOADOUT.keys()), 1])
                        a1iVarDays_IN_LOADOUT[:] = np.nan

                        # Define period to compute SWI filter
                        oVarName_FILTER = {}
                        for iVarIndex_IN_LOADOUT, sVarKeys_IN_LOADOUT in enumerate(oVarName_IN_LOADOUT.keys()):

                            # Get variable out information
                            oKeys_IN_LOADOUT = prepareDictKey([sVarKeys_IN_LOADOUT, 'Days'])
                            iVarDays_IN_LOADOUT = lookupDictKey(oVarName_IN_LOADOUT, *oKeys_IN_LOADOUT)
                            oKeys_IN_LOADOUT = prepareDictKey([sVarKeys_IN_LOADOUT, 'Name'])
                            sVarDays_IN_LOADOUT = lookupDictKey(oVarName_IN_LOADOUT, *oKeys_IN_LOADOUT)

                            a1iVarDays_IN_LOADOUT[iVarIndex_IN_LOADOUT] = iVarDays_IN_LOADOUT * iVarDayStep_IN

                            sTime_FILTER_FROM = Lib_Time_Apps.getTimeFrom(sTime_RET, iVarDays_IN_LOADOUT * iVarDayStep_IN, iTimeDataDyn_IN)[0]
                            sTime_FILTER_TO = Lib_Time_Apps.getTimeTo(sTime_RET, 0, iTimeDataDyn_IN)[0]

                            # Saving filter settings
                            oVarName_FILTER[sVarDays_IN_LOADOUT] = {}
                            oVarName_FILTER[sVarDays_IN_LOADOUT]['TimeSteps'] = iVarDays_IN_LOADOUT * iVarDayStep_IN
                            oVarName_FILTER[sVarDays_IN_LOADOUT]['TimeDays'] = iVarDays_IN_LOADOUT
                            oVarName_FILTER[sVarDays_IN_LOADOUT]['TimeFrom'] = sTime_FILTER_FROM
                            oVarName_FILTER[sVarDays_IN_LOADOUT]['TimeTo'] = sTime_FILTER_TO

                        # Compute maximum of the days
                        iVarDaysMax_IN_LOADOUT = np.max(a1iVarDays_IN_LOADOUT)

                        # Get time information
                        sTime_RET_FROM = Lib_Time_Apps.getTimeFrom(sTime_RET, iVarDaysMax_IN_LOADOUT, iTimeDataDyn_IN)[0]
                        sTime_RET_TO = Lib_Time_Apps.getTimeTo(sTime_RET, 0, iTimeDataDyn_IN)[0]
                        a1oTime_RET_STEPS = Lib_Time_Apps.getTimeSteps(sTime_RET_FROM, sTime_RET_TO, iTimeDataDyn_IN)

                        # Cycle(s) on time step(s)
                        for sTime_RET_STEP in a1oTime_RET_STEPS:

                            # Define filename tags
                            sFileDataDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_RAW),
                                                {'$yyyy': sTime_RET_STEP[0:4],
                                                 '$mm': sTime_RET_STEP[4:6],
                                                 '$dd': sTime_RET_STEP[6:8],
                                                 '$HH': sTime_RET_STEP[8:10],
                                                 '$MM': sTime_RET_STEP[10:12],
                                                 '$DOMAIN': self.oTags['$DOMAIN']})

                            # Define filename with path
                            sFileNameDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_TAGS), self.oTags)
                            sFileNameDyn_TAGS = addFileExtZip(sFileNameDyn_TAGS, sVarName_IN_Zip)[0]

                            # Search all file(s) with selected root
                            a1sFileNameDyn_TAGS = sorted(glob.glob(sFileNameDyn_TAGS))

                            # Store time steps and selected file(s)
                            a1oFileDataDyn_SOURCE[sTime_RET_STEP] = {}
                            a1oFileDataDyn_SOURCE[sTime_RET_STEP] = a1sFileNameDyn_TAGS

                            # Save variable information
                            if not sVarType in a1oVarsInfoDyn_SOURCE:
                                a1oVarsInfoDyn_SOURCE[sVarType] = {}
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_IN'] = oVarName_IN_LOADIN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_OUT'] = oVarName_IN_LOADOUT
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_FilterT'] = oVarName_FILTER
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_InterpMethod'] = oVarMethodInterp_IN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_AggregMethod'] = oVarMethodAggreg_IN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_MissingValue'] = oVarName_IN_MissValue
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_ValidRange'] = oVarName_IN_ValidRng
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_ReadMethod'] = sVarFunc_IN_LOAD
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_SaveMethod'] = ''
                            else:
                                pass

                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Get list unique value(s)
                if a1oFileDataDyn_SOURCE:
                    # Exit message
                    oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... OK')
                    bData_SOURCE = True
                else:
                    a1oFileDataDyn_SOURCE = {}
                    a1oVarsInfoDyn_SOURCE = {}
                    Exc.getExc(' -----> WARNING: no data selected in RETRIEVE DATA!', 2, 1)
                    # Exit message
                    oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... SKIPPED. Data not available!')
                    bData_SOURCE = False

                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Pass variable to global workspace
                self.a1oFileDataDyn_SOURCE = a1oFileDataDyn_SOURCE
                self.a1oVarsInfoDyn_SOURCE = a1oVarsInfoDyn_SOURCE
                self.bData_SOURCE = bData_SOURCE
                # -------------------------------------------------------------------------------------

            else:

                # -------------------------------------------------------------------------------------
                # Exit for previously processed data
                self.a1oFileDataDyn_SOURCE = {}
                self.a1oVarsInfoDyn_SOURCE = {}
                self.bData_SOURCE = True
                oLogStream.info(
                    ' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... SKIPPED. Data previously processed!')
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Exit for previously processed data
            self.a1oFileDataDyn_SOURCE = {}
            self.a1oVarsInfoDyn_SOURCE = {}
            self.bData_SOURCE = True
            oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... SKIPPED. No file(s) selected!')
            # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to get data 
    def getDynamicData(self, sTime):

        # -------------------------------------------------------------------------------------
        # Info start
        os.chdir(self.sPathSrc)
        sTime_GET = sTime
        oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... ')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get information
        a1oFileDataDyn_SOURCE = self.a1oFileDataDyn_SOURCE
        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Cycle(s) on selected file(s)
        a1oFileDataDyn_GET = {}
        a1oFileDataGeo_GET = {}
        if a1oVarsInfoDyn_SOURCE:

            # -------------------------------------------------------------------------------------
            # Cycle(s) on time(s)
            for sTimeDyn_GET in sorted(a1oFileDataDyn_SOURCE):

                # Get filename(s) from source workspace
                a1sFileDataDyn_SOURCE = a1oFileDataDyn_SOURCE[sTimeDyn_GET]

                # Checking file(s) availability
                if a1sFileDataDyn_SOURCE:

                    # Cycle(s) on selected file(s)
                    for sFileDataDyn_GET in a1sFileDataDyn_SOURCE:

                        # Info analyzed file
                        oLogStream.info(' -----> FILE ANALYZED: ' + sFileDataDyn_GET)

                        # Get data
                        try:
                            # Driver to unzip file and close handle
                            oZipDrv_GET = Drv_File_Zip(sFileDataDyn_GET, 'u', None, '.gz').oFileWorkspace
                            [oFileZip_GET_IN, oFileZip_GET_OUT] = oZipDrv_GET.oFileLibrary.openZip(
                                oZipDrv_GET.sFileName_IN,
                                oZipDrv_GET.sFileName_OUT,
                                oZipDrv_GET.sZipMode)
                            oZipDrv_GET.oFileLibrary.zipFile(oFileZip_GET_IN, oFileZip_GET_OUT)
                            oZipDrv_GET.oFileLibrary.closeZip(oFileZip_GET_IN, oFileZip_GET_OUT)

                            # Driver to open unzipped file and read data
                            oFileDrv_GET = Drv_Data_IO(oZipDrv_GET.sFileName_OUT, 'r').oFileWorkspace
                            oFileData_GET = oFileDrv_GET.oFileLibrary.openFile(
                                join(oFileDrv_GET.sFilePath, oFileDrv_GET.sFileName),
                                oFileDrv_GET.sFileMode)

                            removeFileUnzip(oZipDrv_GET.sFileName_OUT, True)

                        except:
                            # Driver to unzipped file and close handle
                            oFileDrv_GET = Drv_Data_IO(sFileDataDyn_GET, 'r').oFileWorkspace
                            oFileData_GET = oFileDrv_GET.oFileLibrary.openFile(
                                join(oFileDrv_GET.sFilePath, oFileDrv_GET.sFileName),
                                oFileDrv_GET.sFileMode)

                        # Cycle(s) on variable(s)
                        a1oFileDataDyn_GET[sTimeDyn_GET] = {}
                        a1oFileDataGeo_GET[sTimeDyn_GET] = {}
                        for sVarNameDyn_SOURCE in a1oVarsInfoDyn_SOURCE:

                            # Get variable information
                            oVarInfoDyn_GET_IN = prepareDictKey([sVarNameDyn_SOURCE, 'Var_IN', 'Var_1'])
                            sVarNameDyn_GET_IN = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_GET_IN)

                            oVarInfoDyn_GET_OUT = prepareDictKey([sVarNameDyn_SOURCE, 'Var_OUT'])
                            sVarNameDyn_GET_OUT = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_GET_OUT)

                            # Get read method and data
                            oFileDrv_GET_ReadMethod = getattr(
                                oFileDrv_GET.oFileLibrary, a1oVarsInfoDyn_SOURCE[sVarNameDyn_SOURCE]['Var_ReadMethod'])
                            a2dVarData_GET = oFileDrv_GET_ReadMethod(oFileData_GET, sVarNameDyn_SOURCE)

                            # Save variable data into workspace
                            if not sVarNameDyn_SOURCE == 'Longitude' and not sVarNameDyn_SOURCE == 'Latitude':
                                a1oFileDataDyn_GET[sTimeDyn_GET][sVarNameDyn_GET_IN] = {}
                                a1oFileDataDyn_GET[sTimeDyn_GET][sVarNameDyn_GET_IN] = a2dVarData_GET
                            else:
                                pass

                            # Save geographical information into workspace
                            if 'Longitude' not in a1oFileDataGeo_GET[sTimeDyn_GET]:
                                a2dGeoX_GET = oFileDrv_GET.oFileLibrary.get2DVar(oFileData_GET, 'Longitude')
                                a1oFileDataGeo_GET[sTimeDyn_GET]['Longitude'] = a2dGeoX_GET
                            else:
                                pass
                            if 'Latitude' not in a1oFileDataGeo_GET[sTimeDyn_GET]:
                                a2dGeoY_GET = oFileDrv_GET.oFileLibrary.get2DVar(oFileData_GET, 'Latitude')
                                a1oFileDataGeo_GET[sTimeDyn_GET]['Latitude'] = a2dGeoY_GET
                            else:
                                pass

                        # Close file in netCDF format
                        oFileDrv_GET.oFileLibrary.closeFile(oFileData_GET)
                        # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------

                else:

                    # -------------------------------------------------------------------------------------
                    # Exit input file(s) not available
                    Exc.getExc(' -----> WARNING: no file available in GET data at time ' + sTimeDyn_GET + ' !', 2, 1)
                    a1oFileDataDyn_GET[sTimeDyn_GET] = []
                    a1oFileDataGeo_GET[sTimeDyn_GET] = []
                    # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Info end
            oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... OK ')
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_GET = a1oFileDataDyn_GET
            self.a1oFileDataGeo_GET = a1oFileDataGeo_GET
            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Exit for previously processed data
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_GET = {}
                self.a1oFileDataGeo_GET = {}
                oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_GET = {}
                self.a1oFileDataGeo_GET = {}
                oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... SKIPPED. Data not available!')
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_GET = open('oDataDyn_GET_H16-SWI.pkl', 'wb')
        #pickle.dump(a1oFileDataDyn_GET, oData_GET)
        #oData_GET.close()
        #oGeo_GET = open('oDataGeo_GET_H16-SWI.pkl', 'wb')
        #pickle.dump(a1oFileDataGeo_GET, oGeo_GET)
        #oGeo_GET.close()
        # DEBUG END #####

        # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to parser data 
    def parserDynamicData(self, sTime):

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oFile_GET = open('oDataDyn_GET_H16-SWI.pkl', 'rb')
        #a1oFileDataDyn_GET = pickle.load(oFile_GET)
        #oFile_GET.close()
        #oGeo_GET = open('oDataGeo_GET_H16-SWI.pkl', 'rb')
        #a1oFileDataGeo_GET = pickle.load(oGeo_GET)
        #oGeo_GET.close()
        #self.a1oFileDataDyn_GET = a1oFileDataDyn_GET
        #self.a1oFileDataGeo_GET = a1oFileDataGeo_GET
        # DEBUG END #####

        # -------------------------------------------------------------------------------------
        # Info
        os.chdir(self.sPathSrc)
        sTime_PAR = sTime
        oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... ')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get information
        oDataGeo = self.oDataGeo

        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE
        a1oFileDataDyn_GET = self.a1oFileDataDyn_GET
        a1oFileDataGeo_GET = self.a1oFileDataGeo_GET

        iDimsDataDyn_GET = len(a1oFileDataDyn_GET)
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check data workspace
        if a1oFileDataDyn_GET:

            # Variable(s) initialization
            a1oFileTimeDyn_PAR = {}
            a1oFileDataDyn_PAR = {}
            a2dVarDataDyn_PAR = np.zeros([oDataGeo.iRows * oDataGeo.iCols, iDimsDataDyn_GET])

            # Cycle(s) on variable(s)
            for sVarInfoDyn_PAR in a1oVarsInfoDyn_SOURCE:

                # Cycle(s) on time(s)
                a1sFileTimeDyn_PAR = []
                for iTimeDyn_PAR, sTimeDyn_PAR in enumerate(sorted(a1oFileDataDyn_GET)):

                    # Get time step workspace
                    oFileDataDyn_PAR = a1oFileDataDyn_GET[sTimeDyn_PAR]
                    oFileDataGeo_PAR = a1oFileDataGeo_GET[sTimeDyn_PAR]

                    # Check file(s) availability
                    if oFileDataDyn_PAR and oFileDataGeo_PAR:

                        # Get interpolation method
                        sVarMethodInterp_PAR = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_PAR]['Var_InterpMethod']['Func']

                        # Get var limit(s) and undefined value
                        dVar_MissValue_PAR = float(a1oVarsInfoDyn_SOURCE[sVarInfoDyn_PAR]['Var_MissingValue'])
                        oVar_ValidRange_PAR = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_PAR]['Var_ValidRange']
                        a1dVar_ValidRange_PAR = np.asarray(oVar_ValidRange_PAR.split(','))

                        # Get values of Latitude, Longitude and Data
                        oVar_PAR = oFileDataDyn_PAR[sVarInfoDyn_PAR]

                        # Method to interpolate data
                        oVarDrv = Drv_Analysis(Lib_Analysis, sVarMethodInterp_PAR,
                                               oGeoX_OUT=oDataGeo.a2dGeoX, oGeoY_OUT=oDataGeo.a2dGeoY,
                                               oGeoNan_OUT=oDataGeo.a2bGeoDataNaN,
                                               oData_IN=oVar_PAR,
                                               oGeoX_IN=oFileDataGeo_PAR['Longitude'],
                                               oGeoY_IN=oFileDataGeo_PAR['Latitude'])

                        oVarMethod = oVarDrv.get_func()
                        oVarArgs = oVarDrv.check_args(oVarMethod)
                        a2dVar_INTERP = oVarDrv.run_func(oVarMethod, oVarArgs)

                        try:
                            a2dVar_INTERP[np.isnan(a2dVar_INTERP)] = np.nan
                            a2dVar_INTERP[np.where(a2dVar_INTERP < float(a1dVar_ValidRange_PAR[0]))] = np.nan
                            a2dVar_INTERP[np.where(a2dVar_INTERP > float(a1dVar_ValidRange_PAR[1]))] = np.nan
                        except:
                            pass

                        # Store data and time in workspace(s) (in Fortran order to compare with matlab arrays)
                        a1dVar_INTERP = np.reshape(a2dVar_INTERP,
                                                   [oFileDataGeo_PAR['Longitude'].shape[0] * oFileDataGeo_PAR['Latitude'].shape[1]],
                                                   order='F')
                        a2dVarDataDyn_PAR[:, iTimeDyn_PAR] = a1dVar_INTERP  # a2dVar_INTERP.ravel()
                        a1sFileTimeDyn_PAR.append(sTimeDyn_PAR)

                        # Debug
                        #a2dVarDataDyn_DEBUG_1 = oFileDataDyn_PAR[sVarInfoDyn_PAR]
                        #a2dVarDataDyn_DEBUG_1[a2dVarDataDyn_DEBUG_1 < 0] = np.nan
                        #a1dVarDataDyn_DEBUG_2 = a2dVarDataDyn_PAR[:, iTimeDyn_PAR]
                        #a2dVarDataDyn_DEBUG_2 = np.reshape(a1dVarDataDyn_DEBUG_2, [oFileDataGeo_PAR['Longitude'].shape[0], oFileDataGeo_PAR['Latitude'].shape[1]])
                        #plt.figure(1); plt.imshow(a2dVar_INTERP); plt.colorbar()
                        #plt.figure(2); plt.imshow(a2dVarDataDyn_DEBUG_1); plt.colorbar()
                        #plt.figure(3); plt.imshow(a2dVarDataDyn_DEBUG_2); plt.colorbar()
                        #plt.figure(4); plt.plot(a1dVar_INTERP);
                        #plt.show()

                    else:

                        # Condition for data not available of a selected time step
                        a1dVarDataDyn_PAR = np.zeros([oDataGeo.iRows * oDataGeo.iCols])
                        a1dVarDataDyn_PAR[:] = np.nan
                        a2dVarDataDyn_PAR[:, iTimeDyn_PAR] = a1dVarDataDyn_PAR
                        a1sFileTimeDyn_PAR.append(sTimeDyn_PAR)
                        Exc.getExc(' -----> WARNING: no data available in PARSER data at time ' + sTimeDyn_PAR + ' !', 2, 1)

                # Put all information in one workspace
                a1oFileDataDyn_PAR[sVarInfoDyn_PAR] = a2dVarDataDyn_PAR
                a1oFileTimeDyn_PAR[sVarInfoDyn_PAR] = a1sFileTimeDyn_PAR
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Info end
            oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... OK ')
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_PAR = a1oFileDataDyn_PAR
            self.a1oFileTimeDyn_PAR = a1oFileTimeDyn_PAR
            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_PAR = {}
                self.a1oFileTimeDyn_PAR = {}
                oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_PAR = {}
                self.a1oFileTimeDyn_PAR = {}
                oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Data not available!')
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_PAR = open('oDataDyn_PAR_H16-SWI.pkl', 'wb')
        #pickle.dump(a1oFileDataDyn_PAR, oData_PAR)
        #oData_PAR.close()
        #oTime_PAR = open('oTimeDyn_PAR_H16-SWI.pkl', 'wb')
        #pickle.dump(a1oFileTimeDyn_PAR, oTime_PAR)
        #oTime_PAR.close()
        #import scipy.io as sio
        #os.chdir(self.sPathClass)
        #oData = {'SSM_Data': a1oFileDataDyn_PAR, 'SSM_Time': a1oFileTimeDyn_PAR}
        #sio.savemat('oDataDyn_PAR_H16-SWI.mat', oData)
        # DEBUG END #####

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to compute data 
    def computeDynamicData(self, sTime):

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oFile_PAR = open('oDataDyn_PAR_H16-SWI.pkl', 'rb')
        #a1oFileDataDyn_PAR = pickle.load(oFile_PAR)
        #oFile_PAR.close()
        #oTime_PAR = open('oTimeDyn_PAR_H16-SWI.pkl', 'rb')
        #a1oFileTimeDyn_PAR = pickle.load(oTime_PAR)
        #oTime_PAR.close()
        #self.a1oFileDataDyn_PAR = a1oFileDataDyn_PAR
        #self.a1oFileTimeDyn_PAR = a1oFileTimeDyn_PAR
        # DEBUG END #####

        # -------------------------------------------------------------------------------------
        # Info
        os.chdir(self.sPathSrc)
        sTime_CMP = sTime
        oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... ')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get information
        a1oFileDataDyn_PAR = self.a1oFileDataDyn_PAR
        a1oFileTimeDyn_PAR = self.a1oFileTimeDyn_PAR
        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE

        oDataGeo = self.oDataGeo
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check data workspace
        if a1oFileDataDyn_PAR and a1oFileTimeDyn_PAR:

            # -------------------------------------------------------------------------------------
            # Cycle(s) on variable(s)
            for sVarNameDyn_PAR in a1oVarsInfoDyn_SOURCE:

                # -------------------------------------------------------------------------------------
                # Get variable information
                oVarInfoDyn_PAR_IN = prepareDictKey([sVarNameDyn_PAR, 'Var_IN', 'Var_1'])
                sVarNameDyn_PAR_IN = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_PAR_IN)

                oVarInfoDyn_PAR_OUT = prepareDictKey([sVarNameDyn_PAR, 'Var_OUT'])
                sVarNameDyn_PAR_OUT = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_PAR_OUT)
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Get data and time of selected variable
                a2dFileDataDyn_PAR = a1oFileDataDyn_PAR[sVarNameDyn_PAR_IN]
                a1sFileTimeDyn_PAR = a1oFileTimeDyn_PAR[sVarNameDyn_PAR_IN]
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Get filter settings
                oVarsFilterDyn_PAR = a1oVarsInfoDyn_SOURCE[sVarNameDyn_PAR]['Var_FilterT']
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Cycle(s) on filtering variable(s)
                oVarSWI_CMP = {}
                for sVarFilterDyn_SOURCE in sorted(oVarsFilterDyn_PAR, reverse=True):

                    # -------------------------------------------------------------------------------------
                    # Get filter settings
                    #sVarFilterDyn_SOURCE = 'SWI_Value_T06'
                    oVarSetting_FILTER = oVarsFilterDyn_PAR[sVarFilterDyn_SOURCE]

                    # Compute soil water index
                    oLogStream.info(
                        ' -----> SWI recursive filter: ' + str(oVarSetting_FILTER['TimeDays']) + ' days ... ')

                    a2dVarSWI_FILTER = computeVarSWI(a2dVarData=a2dFileDataDyn_PAR,
                                                  a1oVarTime=a1sFileTimeDyn_PAR,
                                                  iTimeFilter=oVarSetting_FILTER['TimeDays'],
                                                  sTimeFrom=oVarSetting_FILTER['TimeFrom'],
                                                  sTimeTo=oVarSetting_FILTER['TimeTo'])

                    oLogStream.info(
                        ' -----> SWI recursive filter: ' + str(oVarSetting_FILTER['TimeDays']) + ' days ... OK')
                    # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------
                    # Define SWI map (get values at the actual time step) --> in Fortran order; needs to reshape using F flag
                    a2dVarSWI_CMP = np.reshape(a2dVarSWI_FILTER[:, -1], (oDataGeo.iRows, oDataGeo.iCols), order='F')

                    # Debug
                    #plt.figure(1)
                    #plt.imshow(a2dVarSWI_CMP); plt.colorbar()
                    #plt.show()

                    # Check variable limits
                    a2dVarSWI_CMP[np.where(a2dVarSWI_CMP < 0.0)] = 0.0
                    a2dVarSWI_CMP[np.where(a2dVarSWI_CMP > 100.0)] = 100.0

                    # Save SWI in workspace
                    oVarSWI_CMP[sVarFilterDyn_SOURCE] = {}
                    oVarSWI_CMP[sVarFilterDyn_SOURCE] = a2dVarSWI_CMP
                    # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Info
            oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... OK ')
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_CMP = oVarSWI_CMP
            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_CMP = {}
                oLogStream.info(
                    ' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_CMP = {}
                oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data not available!!')
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oFile_CMP = open('oDataDyn_CMP_H16-SWI.pkl', 'wb')
        #pickle.dump(oVarSWI_CMP, oFile_CMP)
        #oFile_CMP.close()
        #import scipy.io as sio
        #os.chdir(self.sPathClass)
        #oData = {'SWI': oVarSWI_CMP}
        #sio.savemat('oDataDyn_CMP_H16-SWI.mat', oData)
        # DEBUG END #####

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to save data
    def saveDynamicData(self, sTime):

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oFile_CMP = open('oDataDyn_CMP_H16-SWI.pkl', 'rb')
        #a1oFileDataDyn_CMP = pickle.load(oFile_CMP)
        #oFile_CMP.close()
        #self.a1oFileDataDyn_CMP = a1oFileDataDyn_CMP
        # DEBUG END #####

        # -------------------------------------------------------------------------------------
        # Info
        os.chdir(self.sPathSrc)
        sTime_SAVE = sTime
        oLogStream.info(' ====> SAVE DATA AT TIME: ' + sTime_SAVE + ' ...  ')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get information
        a1oFileDataDyn_CMP = self.a1oFileDataDyn_CMP

        # Get path information
        sPathDataDyn_OUT = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicOutcome']
        sPathDataDyn_OUT = defineFolder(sPathDataDyn_OUT, self.oTags)
        sPathCache_HIS = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        sPathCache_HIS = defineFolder(sPathCache_HIS, self.oTags)

        # Get IN variable information
        oVarWorkspace_OUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check data workspace
        if a1oFileDataDyn_CMP:

            # -------------------------------------------------------------------------------------
            # Cycle(s) on file type
            for sFileType in oVarWorkspace_OUT:

                # -------------------------------------------------------------------------------------
                # Get variable(s) information
                oVarsInfo_OUT = oVarWorkspace_OUT[sFileType]
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Check file type
                if sFileType == 'NetCDF':

                    # -------------------------------------------------------------------------------------
                    # List initialization
                    a1bFileCheck_HIS = []
                    a1sFileName_HIS = []
                    a1oVarTime_OUT = []
                    # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------
                    # Get output variable(s)
                    oVarInfo_OUT = oVarWorkspace_OUT[sFileType]

                    # Remove static variable (if present in output dictionary)
                    oVarInfo_OUT = removeDictKeys(oVarInfo_OUT, ['Longitude', 'Latitude', 'Terrain'])
                    # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------
                    # Cycle(s) on variable(s)
                    for sVarName_OUT in oVarInfo_OUT:

                        # -------------------------------------------------------------------------------------
                        # Time Info
                        oLogStream.info(' ------> Save time step (NC): ' + sTime_SAVE)
                        # -------------------------------------------------------------------------------------

                        # -------------------------------------------------------------------------------------
                        # Save time information (for loading and saving function)
                        a1oVarTime_OUT.append(sTime_SAVE)
                        iVarLen_OUT = 1
                        # -------------------------------------------------------------------------------------

                        # -------------------------------------------------------------------------------------
                        # Filename NC OUT
                        sFileNameDyn_OUT = defineFileName(
                            join(sPathDataDyn_OUT, oVarsInfo_OUT[sVarName_OUT]['VarSource']),
                            self.oTags)

                        # Check output file(s) availability 
                        bFileExistDyn_OUT = checkFileName(sFileNameDyn_OUT + '.' +
                                                          oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Zip'])

                        # Info
                        oLogStream.info(' -------> Saving file output (NC): ' + sFileNameDyn_OUT + ' ... ')
                        # -------------------------------------------------------------------------------------

                        # -------------------------------------------------------------------------------------
                        # Check errors in code
                        try:

                            # -------------------------------------------------------------------------------------
                            # Open NC file (in write or append mode)
                            bVarExistNC_OUT = False
                            if not bFileExistDyn_OUT:

                                # -------------------------------------------------------------------------------------
                                # Open NC file in write mode
                                oFileDrv_OUT = Drv_Data_IO(sFileNameDyn_OUT, 'w').oFileWorkspace
                                oFileData_OUT = oFileDrv_OUT.oFileLibrary.openFile(
                                    join(oFileDrv_OUT.sFilePath, oFileDrv_OUT.sFileName),
                                    oFileDrv_OUT.sFileMode)
                                bVarExistNC_OUT = oFileDrv_OUT.oFileLibrary.checkVarName(oFileData_OUT, sVarName_OUT)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Write global attributes (common, extra and arrays)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeFileAttrsCommon(
                                    oFileData_OUT,
                                    self.oDataInfo.oInfoSettings.oGeneralInfo,
                                    split(sFileNameDyn_OUT)[0])

                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeFileAttrsExtra(
                                    oFileData_OUT,
                                    self.oDataInfo.oInfoSettings.oParamsInfo,
                                    self.oDataGeo.a1oGeoHeader)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Write geo-system information
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeGeoSystem(
                                    oFileData_OUT,
                                    self.oDataInfo.oInfoSettings.oGeoSystemInfo,
                                    self.oDataGeo.a1dGeoBox)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Declare variable dimensions
                                sDimVarX = oVarsInfo_OUT['Terrain']['VarDims']['X']
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT,
                                                                                             sDimVarX,
                                                                                             self.oDataGeo.iCols)
                                sDimVarY = oVarsInfo_OUT['Terrain']['VarDims']['Y']
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT,
                                                                                             sDimVarY,
                                                                                             self.oDataGeo.iRows)
                                sDimVarT = 'time'
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT,
                                                                                             sDimVarT, iVarLen_OUT)
                                # Declare extra dimension(s)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT,
                                                                                             'nsim', 1)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT,
                                                                                             'ntime', 2)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT,
                                                                                             'nens', 1)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Write time information
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeTime(oFileData_OUT,
                                                                                             a1oVarTime_OUT, 'f8',
                                                                                             'time',
                                                                                             iVarLen_OUT / iVarLen_OUT)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Try to save longitude
                                sVarGeoX = 'Longitude'
                                a2dGeoX = self.oDataGeo.a2dGeoX
                                oLogStream.info(' -------> Saving variable: ' + sVarGeoX + ' ... ')
                                try:

                                    # -------------------------------------------------------------------------------------
                                    # Get longitude
                                    oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary,
                                                                   oVarsInfo_OUT[sVarGeoX]['VarOp']['Op_Save']['Func'])
                                    oFileDRV_WriteMethod(oFileData_OUT,
                                                         sVarGeoX, a2dGeoX,
                                                         oVarsInfo_OUT[sVarGeoX]['VarAttributes'],
                                                         oVarsInfo_OUT[sVarGeoX]['VarOp']['Op_Save']['Format'],
                                                         oVarsInfo_OUT[sVarGeoX]['VarDims']['Y'],
                                                         oVarsInfo_OUT[sVarGeoX]['VarDims']['X'])
                                    # Info
                                    a1bFileCheck_HIS.append(True)
                                    oLogStream.info(' -------> Saving variable: ' + sVarGeoX + ' ... OK ')
                                    # -------------------------------------------------------------------------------------

                                except:

                                    # -------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileCheck_HIS.append(False)
                                    Exc.getExc(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info(
                                        ' -------> Saving variable: ' + sVarGeoX + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Try to save latitude
                                sVarGeoY = 'Latitude'
                                a2dGeoY = self.oDataGeo.a2dGeoY
                                oLogStream.info(' -------> Saving variable: ' + sVarGeoY + ' ... ')
                                try:

                                    # -------------------------------------------------------------------------------------
                                    # Get latitude
                                    oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary,
                                                                   oVarsInfo_OUT[sVarGeoY]['VarOp']['Op_Save']['Func'])
                                    oFileDRV_WriteMethod(oFileData_OUT,
                                                         sVarGeoY, a2dGeoY,
                                                         oVarsInfo_OUT[sVarGeoY]['VarAttributes'],
                                                         oVarsInfo_OUT[sVarGeoY]['VarOp']['Op_Save']['Format'],
                                                         oVarsInfo_OUT[sVarGeoY]['VarDims']['Y'],
                                                         oVarsInfo_OUT[sVarGeoY]['VarDims']['X'])
                                    # Info
                                    a1bFileCheck_HIS.append(True)
                                    oLogStream.info(' -------> Saving variable: ' + sVarGeoY + ' ... OK ')
                                    # -------------------------------------------------------------------------------------

                                except:

                                    # -------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileCheck_HIS.append(False)
                                    Exc.getExc(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info(
                                        ' -------> Saving variable: ' + sVarGeoY + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Try to save terrain
                                sVarTerrain = 'Terrain'
                                a2dTerrain = self.oDataGeo.a2dGeoData
                                a2dTerrain[self.oDataGeo.a2bGeoDataNaN] = self.oDataGeo.dNoData

                                oLogStream.info(' -------> Saving variable: ' + sVarTerrain + ' ... ')
                                try:

                                    # -------------------------------------------------------------------------------------
                                    # Get terrain  
                                    oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary,
                                                                   oVarsInfo_OUT[sVarTerrain]['VarOp']['Op_Save'][
                                                                       'Func'])
                                    oFileDRV_WriteMethod(oFileData_OUT,
                                                         sVarTerrain, a2dTerrain,
                                                         oVarsInfo_OUT[sVarTerrain]['VarAttributes'],
                                                         oVarsInfo_OUT[sVarTerrain]['VarOp']['Op_Save']['Format'],
                                                         oVarsInfo_OUT[sVarTerrain]['VarDims']['Y'],
                                                         oVarsInfo_OUT[sVarTerrain]['VarDims']['X'])
                                    # Info
                                    a1bFileCheck_HIS.append(True)
                                    oLogStream.info(' -------> Saving variable: ' + sVarTerrain + ' ... OK ')
                                    # -------------------------------------------------------------------------------------

                                except:

                                    # -------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileCheck_HIS.append(False)
                                    Exc.getExc(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info(
                                        ' -------> Saving variable: ' + sVarTerrain + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Try to save 2d/3d variable
                                oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... ')

                                a2VarData_OUT = a1oFileDataDyn_CMP[sVarName_OUT]
                                a2VarData_OUT[self.oDataGeo.a2bGeoDataNaN] = float(
                                    oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])
                                a2VarData_OUT[np.isnan(a2VarData_OUT)] = float(
                                    oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])

                                try:

                                    # -------------------------------------------------------------------------------------
                                    # Get data dynamic
                                    oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary,
                                                                   oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save'][
                                                                       'Func'])
                                    oFileDRV_WriteMethod(oFileData_OUT,
                                                         sVarName_OUT, a2VarData_OUT,
                                                         oVarsInfo_OUT[sVarName_OUT]['VarAttributes'],
                                                         oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Format'],
                                                         oVarsInfo_OUT[sVarName_OUT]['VarDims']['Y'],
                                                         oVarsInfo_OUT[sVarName_OUT]['VarDims']['X'])

                                    # Info
                                    a1bFileCheck_HIS.append(True)
                                    oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... OK ')
                                    # -------------------------------------------------------------------------------------

                                except:

                                    # -------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileCheck_HIS.append(False)
                                    Exc.getExc(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info(
                                        ' -------> Saving variable: ' + sVarName_OUT + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Close NetCDF file
                                oFileDrv_OUT.oFileLibrary.closeFile(oFileData_OUT)

                                # Zip NetCDF file
                                oZipDrv_OUT = Drv_File_Zip(sFileNameDyn_OUT, 'z', None, '.gz').oFileWorkspace
                                [oFileZip_IN, oFileZip_OUT] = oZipDrv_OUT.oFileLibrary.openZip(oZipDrv_OUT.sFileName_IN,
                                                                                               oZipDrv_OUT.sFileName_OUT,
                                                                                               oZipDrv_OUT.sZipMode)
                                oZipDrv_OUT.oFileLibrary.zipFile(oFileZip_IN, oFileZip_OUT)
                                oZipDrv_OUT.oFileLibrary.closeZip(oFileZip_IN, oFileZip_OUT)

                                sFileNameDyn_ZIP = oZipDrv_OUT.sFileName_OUT
                                oLogStream.info(' -------> Zipping in file: ' + sFileNameDyn_ZIP + ' ... OK')

                                removeFileUnzip(sFileNameDyn_OUT, True)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Info
                                a1sFileName_HIS.append(
                                    sFileNameDyn_OUT + '.' + oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Zip'])
                                oLogStream.info(' ------> Saving file output NetCDF: ' + sFileNameDyn_OUT + ' ... OK')
                                # -------------------------------------------------------------------------------------

                            else:

                                # -------------------------------------------------------------------------------------
                                # Unzip NC file (if file is compressed)
                                oZipDrv_OUT = Drv_File_Zip((sFileNameDyn_OUT + '.gz'), 'u', None, '.gz').oFileWorkspace
                                [oFileZip_IN, oFileZip_OUT] = oZipDrv_OUT.oFileLibrary.openZip(
                                    oZipDrv_OUT.sFileName_IN,
                                    oZipDrv_OUT.sFileName_OUT,
                                    oZipDrv_OUT.sZipMode)
                                oZipDrv_OUT.oFileLibrary.zipFile(oFileZip_IN, oFileZip_OUT)
                                oZipDrv_OUT.oFileLibrary.closeZip(oFileZip_IN, oFileZip_OUT)

                                removeFileZip((sFileNameDyn_OUT + '.gz'), True)

                                # Open NC file in append mode
                                oFileDrv_OUT = Drv_Data_IO(sFileNameDyn_OUT, 'a').oFileWorkspace
                                oFileData_OUT = oFileDrv_OUT.oFileLibrary.openFile(
                                    join(oFileDrv_OUT.sFilePath, oFileDrv_OUT.sFileName),
                                    oFileDrv_OUT.sFileMode)
                                bVarExistNC_OUT = oFileDrv_OUT.oFileLibrary.checkVarName(oFileData_OUT, sVarName_OUT)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Check variable availability
                                oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... ')
                                if bVarExistNC_OUT is False:

                                    # -------------------------------------------------------------------------------------
                                    # Try to save 3d variable
                                    a2VarData_OUT = a1oFileDataDyn_CMP[sVarName_OUT]
                                    a2VarData_OUT[self.oDataGeo.a2bGeoDataNaN] = float(
                                        oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])
                                    a2VarData_OUT[np.isnan(a2VarData_OUT)] = float(
                                        oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])
                                    try:

                                        # -------------------------------------------------------------------------------------
                                        # Get data dynamic
                                        oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary,
                                                                       oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save'][
                                                                           'Func'])
                                        oFileDRV_WriteMethod(oFileData_OUT,
                                                             sVarName_OUT, a2VarData_OUT,
                                                             oVarsInfo_OUT[sVarName_OUT]['VarAttributes'],
                                                             oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Format'],
                                                             oVarsInfo_OUT[sVarName_OUT]['VarDims']['Y'],
                                                             oVarsInfo_OUT[sVarName_OUT]['VarDims']['X'])
                                        # Info
                                        a1bFileCheck_HIS.append(True)
                                        oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... OK ')
                                        # -------------------------------------------------------------------------------------

                                    except:

                                        # -------------------------------------------------------------------------------------
                                        # Exit code
                                        a1bFileCheck_HIS.append(False)
                                        Exc.getExc(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                        oLogStream.info(
                                            ' -------> Saving variable: ' + sVarName_OUT + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                        # -------------------------------------------------------------------------------------

                                        # -------------------------------------------------------------------------------------

                                else:
                                    # -------------------------------------------------------------------------------------
                                    # Info
                                    oLogStream.info(
                                        ' -------> Saving variable: ' + sVarName_OUT + ' ... SAVED PREVIOUSLY')
                                    a1bFileCheck_HIS.append(True)
                                    # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Close NetCDF file
                                oFileDrv_OUT.oFileLibrary.closeFile(oFileData_OUT)

                                # Zip NetCDF file
                                oZipDrv_OUT = Drv_File_Zip(sFileNameDyn_OUT, 'z', None, '.gz').oFileWorkspace
                                [oFileZip_IN, oFileZip_OUT] = oZipDrv_OUT.oFileLibrary.openZip(oZipDrv_OUT.sFileName_IN,
                                                                                               oZipDrv_OUT.sFileName_OUT,
                                                                                               oZipDrv_OUT.sZipMode)
                                oZipDrv_OUT.oFileLibrary.zipFile(oFileZip_IN, oFileZip_OUT)
                                oZipDrv_OUT.oFileLibrary.closeZip(oFileZip_IN, oFileZip_OUT)

                                sFileNameDyn_ZIP = oZipDrv_OUT.sFileName_OUT
                                oLogStream.info(' -------> Zipping in file: ' + sFileNameDyn_ZIP + ' ... OK')

                                removeFileUnzip(sFileNameDyn_OUT, True)
                                # -------------------------------------------------------------------------------------

                                # -------------------------------------------------------------------------------------
                                # Info
                                a1sFileName_HIS.append(
                                    sFileNameDyn_OUT + '.' + oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Zip'])
                                oLogStream.info(' ------> Saving file output NetCDF: ' + sFileNameDyn_OUT + ' ... OK')
                                # -------------------------------------------------------------------------------------

                        except:

                            # -------------------------------------------------------------------------------------
                            # Exit code
                            a1bFileCheck_HIS.append(False)
                            # Info
                            Exc.getExc(' ------> WARNING: errors occurred in saving file! Check your output data!', 2, 1)
                            oLogStream.info(
                                ' ------> Saving file output (NC): ' + sFileNameDyn_OUT + ' ... FAILED --- ERRORS OCCURRED IN SAVING DATA!')
                            # -------------------------------------------------------------------------------------

                            # End of check routine
                            # -------------------------------------------------------------------------------------

                    # End of variable out cycle(s)
                    # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------
                    # Check saved data NC
                    if np.all(np.asarray(a1bFileCheck_HIS) == True):
                        # Create hash handle
                        sFileCache_HIS = os.path.join(sPathCache_HIS,
                                                      'Satellite_HSAF-SWI-H16-RAW_FILENC_' + sTime_SAVE + '.history')

                        # Adding filename(s) HIS
                        a1oFileName_HIS = []
                        for sFileDataDyn_HIS in a1sFileName_HIS:
                            a1oFileName_HIS.append(sFileDataDyn_HIS)

                        # Save history file for NC
                        writeFileHistory(sFileCache_HIS, zip(a1oFileName_HIS))
                    else:
                        # Info warning
                        Exc.getExc(' ------> WARNING: some files are not saved on disk! Check your data input!', 2, 1)

                    # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------
                    # Info
                    oLogStream.info(' ====> SAVE DATA AT TIME: ' + sTime_SAVE + ' ...  OK ')
                    # -------------------------------------------------------------------------------------

                else:

                    # -------------------------------------------------------------------------------------
                    # Info
                    oLogStream.info(
                        ' ====> SAVE DATA AT TIME: ' + sTime_SAVE + ' ...  SKIPPED. Format data output UNKNOWN')
                    # -------------------------------------------------------------------------------------

                # End if condition on filetype format
                # ------------------------------------------------------------------------------------

            # End of file type cycle(s)
            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Info
            if self.bData_SOURCE is True:
                oLogStream.info(' ====> SAVE DATA AT TIME: ' + sTime_SAVE + ' ...  SKIPPED. Data previously processed!')
            else:
                oLogStream.info(' ====> SAVE DATA AT TIME: ' + sTime_SAVE + ' ...  SKIPPED. Data not available!')
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

    # End method
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
