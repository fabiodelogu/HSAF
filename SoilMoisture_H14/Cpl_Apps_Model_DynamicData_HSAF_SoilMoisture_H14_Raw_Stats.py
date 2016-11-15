"""
Class Features

Name:          Cpl_Apps_Model_DynamicData_HSAF_SoilMoisture_H14_Raw_Stats
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160629'
Version:       '2.0.0'
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
from copy import deepcopy

import src.Lib_Analysis_Interpolation as Lib_Int
import src.Lib_Analysis_Computation_HSAF_SoilMoisture as Lib_Cmp
from src.Drv_Analysis_Interpolation import Drv_Analysis as Drv_Analysis

import src.Lib_Time_Apps as Lib_Time_Apps
import src.Lib_File_Zip_Apps as Lib_Data_Zip_Utils

from src.Drv_Exception import Exc
from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_File_Zip import Drv_File_Zip

from src.Lib_File_Zip_Apps import removeFileUnzip, removeFileZip

from src.Lib_Op_System_Apps import deleteFileName, defineFileName, checkFileName, defineFolder
from src.Lib_Op_String_Apps import defineString
from src.Lib_File_Log_Apps import getFileHistory, writeFileHistory, checkSavingTime
from src.Lib_Op_Dict_Apps import prepareDictKey, lookupDictKey, removeDictKeys
from src.Lib_Op_List_Apps import getListUnique

# Debug
#import matplotlib.pylab as plt
######################################################################################

# -------------------------------------------------------------------------------------
# Class
class Cpl_Apps_Model_DynamicData_HSAF_SoilMoisture_H14_Raw_Stats:

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
        for sFileType in oVarsWorkspace_CHK:

            # -------------------------------------------------------------------------------------
            # Check file type
            if sFileType == 'NetCDF':

                # Check file
                sFileCache_CHK = os.path.join(sPathCache_CHK, 'Satellite_HSAF-SM-H14-RAW-STATS_FILENC_' + sTime_CHK + '.history')
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

                    # Check file type
                    if sFileType == 'NetCDF':

                        # Get variable(s) information
                        oVarsInfo_IN = oVarWorkspace_IN[sFileType]

                        # Cycle(s) on variable(s)
                        a1sVarName_IN_Zip = []
                        a1sFileDataDyn_RAW = []
                        for sVarType in oVarsInfo_IN:

                            # Get var information
                            oVarInfo_IN = oVarsInfo_IN[sVarType]

                            # Get variable(s) component(s)
                            sVarFunc_IN_LOAD = oVarInfo_IN['VarOp']['Op_Load']['Func']
                            oVarName_IN_COMPIN = oVarInfo_IN['VarOp']['Op_Load']['Comp']['IN']
                            oVarName_IN_TIMEIN = oVarInfo_IN['VarOp']['Op_Load']['Comp']['IN']['Time_1']
                            oVarName_IN_COMPOUT = oVarInfo_IN['VarOp']['Op_Load']['Comp']['OUT']

                            oVarName_IN_MissValue = oVarInfo_IN['VarOp']['Op_Load']['Missing_value']
                            oVarName_IN_ValidRng = oVarInfo_IN['VarOp']['Op_Load']['Valid_range']
                            oVarName_IN_ScaleFactor = oVarInfo_IN['VarOp']['Op_Load']['ScaleFactor']
                            sVarName_IN_Zip = oVarInfo_IN['VarOp']['Op_Load']['Zip']

                            oVarMethodInterp_IN = oVarInfo_IN['VarOp']['Op_Math']['Interpolation']
                            oVarMethodCmp_IN = oVarInfo_IN['VarOp']['Op_Math']['Computation']['Func']

                            # Get generic filename
                            sFileDataDyn_RAW = oVarInfo_IN['VarSource']

                            # Define period to compute statistics
                            sVarTimeFrom_IN_COMPIN = oVarName_IN_TIMEIN['TimeFrom']

                            sVarTimeTo_IN_COMPIN = oVarName_IN_TIMEIN['TimeTo']
                            sVarTimeTo_IN_COMPIN = Lib_Time_Apps.getTimeNow(sVarTimeTo_IN_COMPIN)[0]

                            iVarTimeDelta_IN_COMPIN = oVarName_IN_TIMEIN['TimeDelta']

                            a1oVarTime_IN_COMPIN = Lib_Time_Apps.getTimeSteps(sTimeFrom=sVarTimeFrom_IN_COMPIN,
                                                                              sTimeTo=sVarTimeTo_IN_COMPIN,
                                                                              iTimeDelta=iVarTimeDelta_IN_COMPIN)

                            # Save variable information
                            if not sVarType in a1oVarsInfoDyn_SOURCE:
                                a1oVarsInfoDyn_SOURCE[sVarType] = {}
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_IN'] = oVarName_IN_COMPIN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_OUT'] = oVarName_IN_COMPOUT
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_TIME'] = a1oVarTime_IN_COMPIN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_InterpMethod'] = oVarMethodInterp_IN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_CmpMethod'] = oVarMethodCmp_IN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_MissingValue'] = oVarName_IN_MissValue
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_ValidRange'] = oVarName_IN_ValidRng
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_ScaleFactor'] = oVarName_IN_ScaleFactor
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_ReadMethod'] = sVarFunc_IN_LOAD
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_SaveMethod'] = ''
                            else:
                                pass

                            a1sVarName_IN_Zip.append(sVarName_IN_Zip)
                            a1sFileDataDyn_RAW.append(sFileDataDyn_RAW)

                        # Cycle(s) on variable(s)
                        a1oVarTime_SOURCE = None
                        for sVarType in oVarsInfo_IN:
                            a1oVarTime_IN_VAR = a1oVarsInfoDyn_SOURCE[sVarType]['Var_TIME']
                            [sVarTime_FROM_SOURCE, sVarTime_TO_SOURCE] = Lib_Time_Apps.checkTimeMaxInt(a1oVarTime_SOURCE, a1oVarTime_IN_VAR)
                            a1oVarTime_SOURCE = Lib_Time_Apps.getTimeSteps(sTimeFrom=sVarTime_FROM_SOURCE,
                                                                           sTimeTo=sVarTime_TO_SOURCE,
                                                                           iTimeDelta=iVarTimeDelta_IN_COMPIN)

                        sVarName_IN_Zip = getListUnique(a1sVarName_IN_Zip)[0]
                        sFileDataDyn_RAW = getListUnique(a1sFileDataDyn_RAW)[0]

                        # Cycle over time step(s)
                        a1oFileDataDyn_SOURCE = {}
                        for sVarTime_SOURCE in a1oVarTime_SOURCE:

                            # Define filename tags
                            sFileDataDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_RAW),
                                                             {'$yyyy': sVarTime_SOURCE[0:4],
                                                              '$mm': sVarTime_SOURCE[4:6],
                                                              '$dd': sVarTime_SOURCE[6:8],
                                                              '$HH': sVarTime_SOURCE[8:10],
                                                              '$MM': sVarTime_SOURCE[10:12],
                                                              '$DOMAIN': self.oTags['$DOMAIN']})

                            # Define filename with path
                            sFileNameDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_TAGS), self.oTags)
                            sFileNameDyn_TAGS = Lib_Data_Zip_Utils.addFileExtZip(sFileNameDyn_TAGS, sVarName_IN_Zip)[0]

                            # Search all file(s) with selected root
                            a1sFileNameDyn_TAGS = sorted(glob.glob(sFileNameDyn_TAGS))

                            # Store time steps and selected file(s)
                            a1oFileDataDyn_SOURCE[sVarTime_SOURCE] = {}
                            a1oFileDataDyn_SOURCE[sVarTime_SOURCE] = a1sFileNameDyn_TAGS

                    else:
                        Exc.getExc(' -----> WARNING: data format unknown in RETRIEVE DATA!', 2, 1)

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
                self.a1oFileDataDyn_SOURCE = []
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
        # Check data workspace
        if a1oVarsInfoDyn_SOURCE:

            # -------------------------------------------------------------------------------------
            # Cycle(s) on time(s)
            a1oFileDataDyn_GET = {}
            a1oFileDataGeo_GET = {}
            for sTimeDyn_GET in sorted(a1oFileDataDyn_SOURCE):

                # Get filename(s) from source workspace
                a1sFileDataDyn_GET = a1oFileDataDyn_SOURCE[sTimeDyn_GET]

                # Cycle(s) on selected file(s)
                if a1sFileDataDyn_GET:

                    # Cycle(s) on selected file(s)
                    a1oFileDataDyn_GET[sTimeDyn_GET] = {}
                    a1oFileDataGeo_GET[sTimeDyn_GET] = {}
                    for sFileDataDyn_GET in a1sFileDataDyn_GET:

                        # Info analyzed file
                        oLogStream.info(' -----> FILE ANALYZED: ' + sFileDataDyn_GET)

                        # Unzip file
                        oZipDrv_GET = Drv_File_Zip(sFileDataDyn_GET, 'u', None, '.gz').oFileWorkspace
                        [oFile_GET_IN, oFile_GET_OUT] = oZipDrv_GET.oFileLibrary.openZip(oZipDrv_GET.sFileName_IN,
                                                                                         oZipDrv_GET.sFileName_OUT,
                                                                                         oZipDrv_GET.sZipMode)
                        oZipDrv_GET.oFileLibrary.unzipFile(oFile_GET_IN, oFile_GET_OUT)
                        oZipDrv_GET.oFileLibrary.closeZip(oFile_GET_IN, oFile_GET_OUT)

                        # Open file
                        oDrvData_GET = Drv_Data_IO(oZipDrv_GET.sFileName_OUT).oFileWorkspace
                        oFile_GET = oDrvData_GET.oFileLibrary.openFile(oZipDrv_GET.sFileName_OUT, 'r')

                        # Cycle(s) on variable(s)
                        for iVarNameDyn_SOURCE, sVarNameDyn_SOURCE in enumerate(a1oVarsInfoDyn_SOURCE):

                            # Info variable
                            oLogStream.info(' ------> VARIABLE: ' + sVarNameDyn_SOURCE)

                            # Get variable information
                            oVarInfoDyn_GET_IN = prepareDictKey([sVarNameDyn_SOURCE, 'Var_IN', 'Var_1'])
                            sVarNameDyn_GET_IN = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_GET_IN)

                            # Get read method and data
                            oDrvFile_ReadMethod = getattr(oDrvData_GET.oFileLibrary, a1oVarsInfoDyn_SOURCE[sVarNameDyn_SOURCE]['Var_ReadMethod'])
                            a2dVar_GET = oDrvFile_ReadMethod(oFile_GET, sVarNameDyn_SOURCE)

                            # Save variable data into workspace
                            a1oFileDataDyn_GET[sTimeDyn_GET][sVarNameDyn_GET_IN] = {}
                            a1oFileDataDyn_GET[sTimeDyn_GET][sVarNameDyn_GET_IN] = a2dVar_GET

                            # Save geographical information into workspace
                            if 'Longitude' not in a1oFileDataGeo_GET[sTimeDyn_GET]:
                                a2dGeoX_GET = oDrvData_GET.oFileLibrary.get2DVar(oFile_GET, 'Longitude')
                                a1oFileDataGeo_GET[sTimeDyn_GET]['Longitude'] = a2dGeoX_GET
                            else:
                                pass
                            if 'Latitude' not in a1oFileDataGeo_GET[sTimeDyn_GET]:
                                a2dGeoY_GET = oDrvData_GET.oFileLibrary.get2DVar(oFile_GET, 'Latitude')
                                a1oFileDataGeo_GET[sTimeDyn_GET]['Latitude'] = a2dGeoY_GET
                            else:
                                pass

                        # Close file netCDF and remove unzipped file
                        oDrvData_GET.oFileLibrary.closeFile(oFile_GET)
                        removeFileUnzip(oZipDrv_GET.sFileName_OUT, True)
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

        # -------------------------------------------------------------------------------------

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_GET = open('oDataDyn_GET_H14-STATS.pkl', 'wb')
        #pickle.dump(a1oFileDataDyn_GET, oData_GET)
        #oData_GET.close()
        #oGeo_GET = open('oTimeDyn_GET_H14-STATS.pkl', 'wb')
        #pickle.dump(a1oFileDataGeo_GET, oGeo_GET)
        #oGeo_GET.close()
        #import scipy.io as sio
        #os.chdir(self.sPathClass)
        #oData = {'SM': a1oFileDataDyn_GET['201201010000']}
        #sio.savemat('oDataDyn_GET_H14-STATS.mat', oData)
        # DEBUG END #####

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to parser data 
    def parserDynamicData(self, sTime):

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_GET = open('oDataDyn_GET_H14-STATS.pkl', 'rb')
        #a1oFileDataDyn_GET = pickle.load(oData_GET)
        #oData_GET.close()
        #oGeo_GET = open('oTimeDyn_GET_H14-STATS.pkl', 'rb')
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

            # Cycle(s) on variable(s)
            for sVarInfoDyn_PAR in a1oVarsInfoDyn_SOURCE:

                # Info variable
                oLogStream.info(' ------> VARIABLE: ' + sVarInfoDyn_PAR)

                # Cycle(s) on time(s)
                a1sFileTimeDyn_PAR = []
                a2dVarDataDyn_PAR = np.zeros([oDataGeo.iRows * oDataGeo.iCols, iDimsDataDyn_GET])
                for iFileTimeDyn_PAR, sFileTimeDyn_PAR in enumerate(sorted(a1oFileDataDyn_GET)):

                    # Get file data and geographical information
                    oFileDataDyn_PAR = a1oFileDataDyn_GET[sFileTimeDyn_PAR]
                    oFileDataGeo_PAR = a1oFileDataGeo_GET[sFileTimeDyn_PAR]

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
                        oVarDrv = Drv_Analysis(Lib_Int, sVarMethodInterp_PAR,
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

                        #plt.figure(1)
                        #plt.imshow(oVar_PAR); plt.colorbar(); plt.clim(0, 100)
                        #plt.figure(2)
                        #plt.imshow(a2dVar_INTERP); plt.colorbar(); plt.clim(0, 100)
                        #plt.show()

                        # Store data and time in workspace(s)
                        a2dVarDataDyn_PAR[:, iFileTimeDyn_PAR] = a2dVar_INTERP.ravel()
                        a1sFileTimeDyn_PAR.append(sFileTimeDyn_PAR)

                    else:
                        a1dVarDataDyn_PAR = np.zeros([oDataGeo.iRows * oDataGeo.iCols])
                        a1dVarDataDyn_PAR[:] = np.nan
                        a2dVarDataDyn_PAR[:, iFileTimeDyn_PAR] = a1dVarDataDyn_PAR
                        a1sFileTimeDyn_PAR.append(sFileTimeDyn_PAR)
                        Exc.getExc(' -----> WARNING: no data available in PARSER data at time ' + sFileTimeDyn_PAR + ' !', 2, 1)

                # Put all information in one workspace
                a1oFileDataDyn_PAR[sVarInfoDyn_PAR] = deepcopy(a2dVarDataDyn_PAR)
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
                oLogStream.info(
                    ' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_PAR = {}
                self.a1oFileTimeDyn_PAR = {}
                oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Data not available!')
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_PAR = open('oDataDyn_PAR_H14-STATS.pkl', 'wb')
        #pickle.dump(a1oFileDataDyn_PAR, oData_PAR)
        #oData_PAR.close()
        #oTime_PAR = open('oTimeDyn_PAR_H14-STATS.pkl', 'wb')
        #pickle.dump(a1oFileTimeDyn_PAR, oTime_PAR)
        #oTime_PAR.close()
        #import scipy.io as sio
        #os.chdir(self.sPathClass)
        #oData = {'SM': a1oFileDataDyn_PAR}
        #sio.savemat('oDataDyn_PAR_H14-STATS.mat', oData)
        # DEBUG END #####

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to compute data 
    def computeDynamicData(self, sTime):

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oFile_PAR = open('oDataDyn_PAR_H14-STATS.pkl', 'rb')
        #a1oFileDataDyn_PAR = pickle.load(oFile_PAR)
        #oFile_PAR.close()
        #os.chdir(self.sPathClass)
        #oTime_PAR = open('oTimeDyn_PAR_H14-STATS.pkl', 'rb')
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
        oDataGeo = self.oDataGeo

        a1oFileDataDyn_PAR = self.a1oFileDataDyn_PAR
        a1oFileTimeDyn_PAR = self.a1oFileTimeDyn_PAR
        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check data workspace
        if a1oFileDataDyn_PAR and a1oFileTimeDyn_PAR:

            # -------------------------------------------------------------------------------------
            # Cycle(s) on variable(s)
            oDataStats_CMP = {}
            for sVarNameDyn_PAR in a1oVarsInfoDyn_SOURCE:

                # -------------------------------------------------------------------------------------
                # Info variable
                oLogStream.info(' ------> VARIABLE: ' + sVarNameDyn_PAR)
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Get variable information
                oVarInfoDyn_PAR_IN = prepareDictKey([sVarNameDyn_PAR, 'Var_IN', 'Var_1'])
                sVarNameDyn_PAR_IN = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_PAR_IN)

                oVarInfoDyn_PAR_OUT = prepareDictKey([sVarNameDyn_PAR, 'Var_OUT'])
                oVarNameDyn_PAR_OUT = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_PAR_OUT)
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Get data and time of selected variable
                a2dFileDataDyn_PAR = a1oFileDataDyn_PAR[sVarNameDyn_PAR_IN]
                oFileTimeDyn_PAR = a1oFileTimeDyn_PAR[sVarNameDyn_PAR_IN]
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Get filter settings
                oVarTimeDyn_PAR = a1oVarsInfoDyn_SOURCE[sVarNameDyn_PAR]['Var_TIME']
                oVarCmpDyn_PAR = a1oVarsInfoDyn_SOURCE[sVarNameDyn_PAR]['Var_CmpMethod']
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Select data over variable time period
                iVarIndexDyn_FROM_CMP = oFileTimeDyn_PAR.index(oVarTimeDyn_PAR[0])
                iVarIndexDyn_TO_CMP = oFileTimeDyn_PAR.index(oVarTimeDyn_PAR[-1])

                a2dFileDataDyn_CMP = deepcopy(a2dFileDataDyn_PAR)
                a2dFileDataDyn_CMP = a2dFileDataDyn_CMP[:, iVarIndexDyn_FROM_CMP : iVarIndexDyn_TO_CMP]
                # -------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Cycle(s) over output variable(s)
                for sVarKeyDyn_CMP_OUT, sVarNameDyn_CMP_OUT in oVarNameDyn_PAR_OUT.iteritems():
                    sVarFunc_CMP = oVarCmpDyn_PAR[sVarKeyDyn_CMP_OUT]
                    oData_CmpMethod = getattr(Lib_Cmp, sVarFunc_CMP)
                    a1dFileStatsDyn_CMP = oData_CmpMethod(a2dFileDataDyn_CMP, 1)
                    a2dFileStatsDyn_CMP = np.reshape(a1dFileStatsDyn_CMP, (oDataGeo.iRows, oDataGeo.iCols))

                    # Debug
                    #plt.figure(1)
                    #plt.imshow(a2dFileStatsDyn_CMP); plt.colorbar()
                    #plt.show()

                    # Check variable limits
                    a2dFileStatsDyn_CMP[np.where(a2dFileStatsDyn_CMP < 0.0)] = 0.0
                    a2dFileStatsDyn_CMP[np.where(a2dFileStatsDyn_CMP > 100.0)] = 100.0

                    # Save statistics in workspace
                    oDataStats_CMP[sVarNameDyn_CMP_OUT] = {}
                    oDataStats_CMP[sVarNameDyn_CMP_OUT] = a2dFileStatsDyn_CMP
                # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Info
            oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... OK ')
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_CMP = oDataStats_CMP
            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_CMP = {}
                oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_CMP = {}
                oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data not available!!')
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_CMP = open('oDataDyn_CMP_H14-STATS.pkl', 'wb')
        #pickle.dump(oDataStats_CMP, oData_CMP)
        #oData_CMP.close()
        # DEBUG END #####

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to save data
    def saveDynamicData(self, sTime):

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oFile_PAR = open('oDataDyn_CMP_H14-STATS.pkl', 'rb')
        #a1oFileDataDyn_CMP = pickle.load(oFile_PAR)
        #oFile_PAR.close()
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
                                    oFileDRV_WriteMethod(oFileDrv_OUT.oFileData,
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
                                    oLogStream.info(' -------> Saving variable: ' + sVarGeoY + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
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
                                    oLogStream.info(' -------> Saving variable: ' + sVarTerrain + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
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
                                    oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
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
                            oLogStream.info(' ------> Saving file output (NC): ' + sFileNameDyn_OUT + ' ... FAILED --- ERRORS OCCURRED IN SAVING DATA!')
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
                                                      'Satellite_HSAF-SM-H14-RAW-STATS_FILENC_' + sTime_SAVE + '.history')

                        # Adding filename(s) HIS
                        a1oFileName_HIS = []
                        for sFileDataDyn_HIS in a1sFileName_HIS:
                            a1oFileName_HIS.append(sFileDataDyn_HIS)

                        # Save history file for NC
                        writeFileHistory(sFileCache_HIS, zip(a1oFileName_HIS))
                    else:
                        # Info warning
                        Exc.getExc(' ------> WARNING: some files are not saved on disk! Check your data input!', 2, 1)

                    # SAVE DATA IN NC FORMAT (END)
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

            # End of filetype cycle(s)
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
