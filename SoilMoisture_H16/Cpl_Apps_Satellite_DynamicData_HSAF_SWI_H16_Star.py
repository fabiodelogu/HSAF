"""
Class Features

Name:          Cpl_Apps_Satellite_DynamicData_HSAF_SWI_H16_Star
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20161024'
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

from copy import deepcopy
from os.path import join, split

import src.Lib_Analysis_Interpolation as Lib_Analysis_Int
import src.Lib_Var_Apps_Conversion as Lib_Var_Cnv
import src.Lib_Analysis_Computation_HSAF_SoilMoisture as Lib_Analysis_Cmp
from src.Drv_Analysis_Interpolation import Drv_Analysis as Drv_Analysis_Int
from src.Drv_Analysis_Computation import Drv_Analysis as Drv_Analysis_Cmp

from src.Drv_Exception import Exc
from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_File_Zip import Drv_File_Zip

from src.Lib_File_Zip_Apps import removeFileUnzip, removeFileZip, addFileExtZip

from src.Lib_Op_System_Apps import deleteFileName, defineFileName, checkFileName, defineFolder
from src.Lib_Op_String_Apps import defineString
from src.Lib_File_Log_Apps import getFileHistory, writeFileHistory, checkSavingTime
from src.Lib_Op_Dict_Apps import prepareDictKey, lookupDictKey, removeDictKeys

# Debug
#import matplotlib.pylab as plt
######################################################################################

# -------------------------------------------------------------------------------------
# Class
class Cpl_Apps_Satellite_DynamicData_HSAF_SWI_H16_Star:

    # -------------------------------------------------------------------------------------
    # Class variable(s)
    oTags = None
    bData_SOURCE = True

    a1oFileDataDyn_CHK = None
    a1oFileDataDyn_SOURCE = None
    a1oVarsInfoDyn_SOURCE = None

    a1oFileStatsDyn_GET = None
    a1oFileStatsGeo_GET = None
    a1oFileDataDyn_GET = None
    a1oFileDataGeo_GET = None

    a1oFileDataDyn_PAR = None
    a1oVarsInfoDyn_PAR = None
    a1oFileStatsDyn_PAR = None

    a1oFileDataDyn_CMP = None
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTime=None, oDataGeo=None, oDataAncillary=None, oDataInfo=None):

        # Data settings and data reference
        self.oDataTime = oDataTime
        self.oDataGeo = oDataGeo
        self.oDataAncillary = oDataAncillary
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
                sFileCache_CHK = os.path.join(sPathCache_CHK, 'Satellite_HSAF-SWI-H16-STAR_FILENC_' + sTime_CHK + '.history')
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

                        # Get variable(s) component(s)
                        sVarFunc_IN_LOAD = oVarInfo_IN['VarOp']['Op_Load']['Func']
                        oVarName_IN_LOADIN = oVarInfo_IN['VarOp']['Op_Load']['Comp']['IN']
                        oVarName_IN_LOADOUT = oVarInfo_IN['VarOp']['Op_Load']['Comp']['OUT']
                        oVarName_IN_MissValue = oVarInfo_IN['VarOp']['Op_Load']['Missing_value']
                        oVarName_IN_ValidRng = oVarInfo_IN['VarOp']['Op_Load']['Valid_range']
                        sVarName_IN_Zip = oVarInfo_IN['VarOp']['Op_Load']['Zip']

                        # Get variable(s) mathematical operation(s)
                        oVarMethodInterp_IN = oVarInfo_IN['VarOp']['Op_Math']['Interpolation']
                        oVarMethodCnv_IN = oVarInfo_IN['VarOp']['Op_Math']['Conversion']
                        oVarMethodCmp_IN = oVarInfo_IN['VarOp']['Op_Math']['Computation']

                        # Get generic filename
                        sFileDataDyn_RAW = oVarInfo_IN['VarSource']

                        # Define filename tags
                        sFileDataDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_RAW),
                                            {'$yyyy': sTime_RET[0:4],
                                             '$mm': sTime_RET[4:6],
                                             '$dd': sTime_RET[6:8],
                                             '$HH': sTime_RET[8:10],
                                             '$MM': sTime_RET[10:12],
                                             '$DOMAIN': self.oTags['$DOMAIN']})

                        # Define filename with path
                        sFileNameDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_TAGS), self.oTags)
                        sFileNameDyn_TAGS = addFileExtZip(sFileNameDyn_TAGS, sVarName_IN_Zip)[0]

                        # Search all file(s) with selected root
                        a1sFileNameDyn_TAGS = sorted(glob.glob(sFileNameDyn_TAGS))

                        # Check file selection
                        if len(a1sFileNameDyn_TAGS) > 0:

                            # Store time steps and selected file(s)
                            a1oFileDataDyn_SOURCE[sTime_RET] = {}
                            a1oFileDataDyn_SOURCE[sTime_RET] = a1sFileNameDyn_TAGS

                            # Save variable information
                            if not sVarType in a1oVarsInfoDyn_SOURCE:
                                a1oVarsInfoDyn_SOURCE[sVarType] = {}
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_IN'] = oVarName_IN_LOADIN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_OUT'] = oVarName_IN_LOADOUT
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_InterpMethod'] = oVarMethodInterp_IN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_CnvMethod'] = oVarMethodCnv_IN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_CmpMethod'] = oVarMethodCmp_IN
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_MissingValue'] = oVarName_IN_MissValue
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_ValidRange'] = oVarName_IN_ValidRng
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_ReadMethod'] = sVarFunc_IN_LOAD
                                a1oVarsInfoDyn_SOURCE[sVarType]['Var_SaveMethod'] = ''
                            else:
                                pass
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
        oVarWorkspace_STATIC = self.oDataInfo.oInfoVarStatic.oDataInputStatic
        oVarWorkspace_ANC = self.oDataAncillary

        a1oFileDataDyn_SOURCE = self.a1oFileDataDyn_SOURCE
        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get data ancillary
        if oVarWorkspace_ANC:

            # Variable(s) initialization
            a1oFileStatsDyn_GET = {}
            a1oFileStatsGeo_GET = {}

            # Case HDF5 format
            if 'HDF5' in oVarWorkspace_STATIC:

                oVar_STATIC = oVarWorkspace_STATIC['HDF5']
                for sVar_STATIC in oVar_STATIC:

                    if hasattr(oVarWorkspace_ANC, sVar_STATIC):
                        oData_STATS = getattr(oVarWorkspace_ANC, sVar_STATIC)

                        for sVar_STATS in oData_STATS:

                            if sVar_STATS == 'Longitude' not in a1oFileStatsGeo_GET:
                                a1oFileStatsGeo_GET['Longitude'] = {}
                                a1oFileStatsGeo_GET['Longitude'] = oData_STATS['Longitude']
                            else:
                                pass
                            if sVar_STATS == 'Latitude' not in a1oFileStatsStatic_GET:
                                a1oFileStatsGeo_GET['Latitude'] = {}
                                a1oFileStatsGeo_GET['Latitude'] = oData_STATS['Latitude']
                            else:
                                pass
                            if sVar_STATS != 'Longitude' and sVar_STATS != 'Latitude':
                                a1oFileStatsDyn_GET[sVar_STATS] = {}
                                a1oFileStatsDyn_GET[sVar_STATS] = oData_STATS[sVar_STATS]
                            else:
                                pass
                    else:
                        pass

            # Case NetCDF format
            elif 'NetCDF' in oVarWorkspace_STATIC:

                oVar_STATIC = oVarWorkspace_STATIC['NetCDF']
                for sVar_STATIC in oVar_STATIC:

                    if hasattr(oVarWorkspace_ANC, sVar_STATIC):
                        oData_STATS = getattr(oVarWorkspace_ANC, sVar_STATIC)

                        for sVar_STATS in oData_STATS:

                            if sVar_STATS == 'Longitude' not in a1oFileStatsGeo_GET:
                                a1oFileStatsGeo_GET['Longitude'] = {}
                                a1oFileStatsGeo_GET['Longitude'] = oData_STATS['Longitude']
                            else:
                                pass
                            if sVar_STATS == 'Latitude' not in a1oFileStatsGeo_GET:
                                a1oFileStatsGeo_GET['Latitude'] = {}
                                a1oFileStatsGeo_GET['Latitude'] = oData_STATS['Latitude']
                            else:
                                pass
                            if sVar_STATS != 'Longitude' and sVar_STATS != 'Latitude':
                                a1oFileStatsDyn_GET[sVar_STATS] = {}
                                a1oFileStatsDyn_GET[sVar_STATS] = oData_STATS[sVar_STATS]
                            else:
                                pass
                    else:
                        pass
            else:
                Exc.getExc(' -----> WARNING: statistical file format not correctly defined!', 2, 1)
        else:
            Exc.getExc(' -----> WARNING: statistical data are not available!', 2, 1)
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check data workspace
        if a1oVarsInfoDyn_SOURCE:

            # -------------------------------------------------------------------------------------
            # Cycle(s) on time(s)
            a1oFileDataDyn_GET = {}
            for sTimeDyn_GET in sorted(a1oFileDataDyn_SOURCE):

                # Get filename(s) from source workspace
                a1sFileDataDyn_GET = a1oFileDataDyn_SOURCE[sTimeDyn_GET]

                # Cycle(s) on selected file(s)
                a1oFileDataDyn_GET = {}
                a1oFileDataGeo_GET = {}
                if a1sFileDataDyn_GET:

                    # Cycle(s) on selected file(s)
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
                        a1oFileDataDyn_GET[sFileDataDyn_GET] = {}
                        a1oFileDataGeo_GET[sFileDataDyn_GET] = {}
                        for sVarNameDyn_SOURCE in a1oVarsInfoDyn_SOURCE:

                            # Get variable information
                            oVarInfoDyn_GET_IN = prepareDictKey([sVarNameDyn_SOURCE, 'Var_IN', 'Var_1'])
                            sVarNameDyn_GET_IN = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_GET_IN)
                            oVarInfoDyn_GET_OUT = prepareDictKey([sVarNameDyn_SOURCE, 'Var_OUT', 'Var_1'])
                            sVarNameDyn_GET_OUT = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_GET_OUT)

                            # Get read method and data
                            oDrvFile_ReadMethod = getattr(oDrvData_GET.oFileLibrary,
                                                          a1oVarsInfoDyn_SOURCE[sVarNameDyn_SOURCE][
                                                              'Var_ReadMethod'])
                            a2dVar_GET = oDrvFile_ReadMethod(oFile_GET, sVarNameDyn_SOURCE)

                            # Save variable data into workspace
                            a1oFileDataDyn_GET[sFileDataDyn_GET][sVarNameDyn_GET_IN] = {}
                            a1oFileDataDyn_GET[sFileDataDyn_GET][sVarNameDyn_GET_IN] = a2dVar_GET

                            # Save geographical information into workspace
                            if 'Longitude' not in a1oFileDataGeo_GET[sFileDataDyn_GET]:
                                a2dGeoX_GET = oDrvData_GET.oFileLibrary.get2DVar(oFile_GET, 'Longitude')
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Longitude'] = a2dGeoX_GET
                            else:
                                pass
                            if 'Latitude' not in a1oFileDataGeo_GET[sFileDataDyn_GET]:
                                a2dGeoY_GET = oDrvData_GET.oFileLibrary.get2DVar(oFile_GET, 'Latitude')
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Latitude'] = a2dGeoY_GET
                            else:
                                pass

                        # Close file netCDF and remove unzipped file
                        oDrvData_GET.oFileLibrary.closeFile(oFile_GET)
                        removeFileUnzip(oZipDrv_GET.sFileName_OUT, True)
                        # -------------------------------------------------------------------------------------
                else:
                    pass
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Info end
            oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... OK ')
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_GET = a1oFileDataDyn_GET
            self.a1oFileDataGeo_GET = a1oFileDataGeo_GET
            self.a1oFileStatsDyn_GET = a1oFileStatsDyn_GET
            self.a1oFileStatsGeo_GET = a1oFileStatsGeo_GET
            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Exit for previously processed data
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_GET = {}
                self.a1oFileDataGeo_GET = {}
                self.a1oFileStatsDyn_GET = {}
                self.a1oFileStatsGeo_GET = {}
                oLogStream.info(
                    ' ====> GET DATA AT TIME: ' + sTime_GET + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_GET = {}
                self.a1oFileDataGeo_GET = {}
                self.a1oFileStatsDyn_GET = {}
                self.a1oFileStatsGeo_GET = {}
                oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... SKIPPED. Data not available!')
            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to parser data 
    def parserDynamicData(self, sTime):

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

        a1oFileStatsDyn_GET = self.a1oFileStatsDyn_GET
        a1oFileStatsGeo_GET = self.a1oFileStatsGeo_GET
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check data workspace
        if a1oFileDataDyn_GET and a1oFileStatsDyn_GET:

            # Cycle(s) on selected file(s)
            a1oFileDataDyn_PAR = {}
            a1oVarsInfoDyn_PAR = {}
            for sFileDataDyn_GET in a1oFileDataDyn_GET:

                # Get file data and geographical information
                oFileDataDyn_GET = a1oFileDataDyn_GET[sFileDataDyn_GET]
                oFileDataGeo_GET = a1oFileDataGeo_GET[sFileDataDyn_GET]

                # Cycle(s) on variable(s)
                a1oFileDataDyn_PAR[sFileDataDyn_GET] = {}
                for sVarInfoDyn_SOURCE in a1oVarsInfoDyn_SOURCE:

                    # Get variable out information
                    oKeys_SOURCE = prepareDictKey([sVarInfoDyn_SOURCE, 'Var_IN'])
                    oVarName_SOURCE = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oKeys_SOURCE)

                    oKeys_PAR = prepareDictKey([sVarInfoDyn_SOURCE, 'Var_OUT'])
                    oVarName_PAR = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oKeys_PAR)

                    # Cycle(s) on variable component(s)
                    for sVarName_SOURCE in oVarName_SOURCE.values():

                        # Condition to avoid geographical information
                        if sVarName_SOURCE != 'Longitude' and sVarName_SOURCE != 'Latitude':

                            # Get interpolation and conversion method(s)
                            sVarMethodInterp_SOURCE = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_InterpMethod']['Func']

                            # Get var limit(s) and undefined value
                            dVar_MissValue = float(a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_MissingValue'])
                            oVar_ValidRange = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_ValidRange']
                            a1dVar_ValidRange = np.asarray(oVar_ValidRange.split(','))

                            # Get values of Latitude, Longitude and Data
                            oVar_GET = oFileDataDyn_GET[sVarName_SOURCE]

                            # Data interpolation
                            oVarDrv = Drv_Analysis_Int(Lib_Analysis_Int, sVarMethodInterp_SOURCE,
                                                       oGeoX_OUT=oDataGeo.a2dGeoX, oGeoY_OUT=oDataGeo.a2dGeoY,
                                                       oGeoNan_OUT=oDataGeo.a2bGeoDataNaN,
                                                       oData_IN=oVar_GET,
                                                       oGeoX_IN=oFileDataGeo_GET['Longitude'],
                                                       oGeoY_IN=oFileDataGeo_GET['Latitude'])

                            oVarMethod = oVarDrv.get_func()
                            oVarArgs = oVarDrv.check_args(oVarMethod)
                            a2dVar_INTERP = oVarDrv.run_func(oVarMethod, oVarArgs)
                            try:
                                a2dVar_INTERP[np.isnan(a2dVar_INTERP)] = np.nan
                                a2dVar_INTERP[np.where(a2dVar_INTERP < float(a1dVar_ValidRange[0]))] = np.nan
                                a2dVar_INTERP[np.where(a2dVar_INTERP > float(a1dVar_ValidRange[1]))] = np.nan
                            except:
                                pass

                            # Debug ####
                            #plt.figure(1)
                            #plt.imshow(oVar_GET); plt.colorbar(); plt.clim(0, 100);
                            #plt.figure(2)
                            #plt.imshow(a2dVar_INTERP); plt.colorbar(); plt.clim(0, 100);
                            #plt.show()
                            ############

                            # Switch variable from SOURCE to PAR
                            sVarName_PAR = oVarName_PAR.values()[0]

                            # Store data in interpolated variable(s) workspace
                            a1oFileDataDyn_PAR[sFileDataDyn_GET][sVarName_PAR] = {}
                            a1oFileDataDyn_PAR[sFileDataDyn_GET][sVarName_PAR] = a2dVar_INTERP

                            # Store dictionary for variable IN and OUT
                            if not oVarName_SOURCE.values()[0] in a1oVarsInfoDyn_PAR:
                                a1oVarsInfoDyn_PAR[oVarName_SOURCE.values()[0]] = {}
                                a1oVarsInfoDyn_PAR[oVarName_SOURCE.values()[0]] = sVarName_PAR
                            else:
                                pass

                        else:
                            pass

            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Cycle(s) on variable(s)
            a1oFileStatsDyn_PAR = {}
            for sVar_STATS in a1oFileStatsDyn_GET:

                oStatsDrv = Drv_Analysis_Int(Lib_Analysis_Int, 'interpVarGridNN',
                                             oGeoX_OUT=oDataGeo.a2dGeoX,
                                             oGeoY_OUT=oDataGeo.a2dGeoY,
                                             oGeoNan_OUT=oDataGeo.a2bGeoDataNaN,
                                             oData_IN=a1oFileStatsDyn_GET[sVar_STATS],
                                             oGeoX_IN=a1oFileStatsGeo_GET['Longitude'],
                                             oGeoY_IN=a1oFileStatsGeo_GET['Latitude'])

                oVarMethod = oStatsDrv.get_func()
                oVarArgs = oStatsDrv.check_args(oVarMethod)
                a2dStats_INTERP = oStatsDrv.run_func(oVarMethod, oVarArgs)

                # Debug
                #plt.figure(3); plt.imshow(a1oFileStatsDyn_GET[sVar_STATS]); plt.colorbar()
                #plt.figure(4); plt.imshow(a2dStats_INTERP); plt.colorbar()
                #plt.show()

                a1oFileStatsDyn_PAR[sVar_STATS] = a2dStats_INTERP
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Info end
            oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... OK ')
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_PAR = a1oFileDataDyn_PAR
            self.a1oVarsInfoDyn_PAR = a1oVarsInfoDyn_PAR
            self.a1oFileStatsDyn_PAR = a1oFileStatsDyn_PAR
            # -------------------------------------------------------------------------------------

            # DEBUG START ###
            #import pickle
            #os.chdir(self.sPathClass)
            #oData_PAR_1 = open('oData_PAR_SWI.pkl', 'wb')
            #pickle.dump(a1oFileDataDyn_PAR, oData_PAR_1)
            #oData_PAR_1.close()
            #oData_PAR_2 = open('oStats_PAR_SWI.pkl', 'wb')
            #pickle.dump(self.a1oFileStatsDyn_PAR, oData_PAR_2)
            #oData_PAR_2.close()
            #oData_PAR_3 = open('oVars_PAR_SWI.pkl', 'wb')
            #pickle.dump(self.a1oVarsInfoDyn_PAR, oData_PAR_3)
            #oData_PAR_3.close()
            # DEBUG END #####

        else:

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_PAR = {}
                self.a1oVarsInfoDyn_PAR = {}
                self.a1oFileStatsDyn_PAR = {}
                oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED.sVarsKeysDyn_CMP Data previously processed!')
            else:
                if not a1oFileDataDyn_GET:
                    self.a1oFileDataDyn_PAR = {}
                    self.a1oVarsInfoDyn_PAR = {}
                    self.a1oFileStatsDyn_PAR = {}
                    oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Data not available!')
                if not a1oFileStatsDyn_GET:
                    self.a1oFileStatsDyn_GET = {}
                    self.a1oVarsInfoDyn_PAR = {}
                    self.a1oFileStatsDyn_PAR = {}
                    oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Stats not available!')
                # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to compute data 
    def computeDynamicData(self, sTime):

        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_PAR_1 = open('oData_PAR_SWI.pkl', 'rb')
        #a1oFileDataDyn_PAR = pickle.load(oData_PAR_1)
        #oData_PAR_1.close()
        #oData_PAR_2 = open('oStats_PAR_SWI.pkl', 'rb')
        #a1oFileStatsDyn_PAR = pickle.load(oData_PAR_2)
        #oData_PAR_2.close()
        #oData_PAR_3 = open('oVars_PAR_SWI.pkl', 'rb')
        #a1oVarsInfoDyn_PAR = pickle.load(oData_PAR_3)
        #oData_PAR_3.close()
        #self.a1oFileDataDyn_PAR = a1oFileDataDyn_PAR
        #self.a1oFileStatsDyn_PAR = a1oFileStatsDyn_PAR
        #self.a1oVarsInfoDyn_PAR = a1oVarsInfoDyn_PAR
        # DEBUG END #####

        # -------------------------------------------------------------------------------------
        # Info
        os.chdir(self.sPathSrc)
        sTime_CMP = sTime
        oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... ')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Get information
        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE
        a1oFileDataDyn_PAR = self.a1oFileDataDyn_PAR
        a1oVarsInfoDyn_PAR = self.a1oVarsInfoDyn_PAR
        a1oFileStatsDyn_PAR = self.a1oFileStatsDyn_PAR
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check data workspace
        if a1oFileDataDyn_PAR and a1oFileStatsDyn_PAR:

            # -------------------------------------------------------------------------------------
            # Cycle(s) on filename(s)
            a1oFileDataDyn_CMP = {}
            for iFileDataDyn_PAR, sFileDataDyn_PAR in enumerate(a1oFileDataDyn_PAR):

                # -------------------------------------------------------------------------------------
                # Cycle(s) on variable(s)
                for sVarInfoDyn_PAR, sVarInfoDyn_CMP in a1oVarsInfoDyn_PAR.iteritems():

                    # -------------------------------------------------------------------------------------
                    # Get information to compute result(s)
                    sVarMethodCmp_PAR = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_PAR]['Var_CmpMethod']['Func']
                    oVarCompCmp_PAR = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_PAR]['Var_CmpMethod']['Comp']
                    sVarMethodCnv_PAR = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_PAR]['Var_CnvMethod']['Func']

                    # Cycle(s) on variable component(s) to get stats
                    oVarStats_PAR = {'Var_1': None, 'Var_2': None, 'Var_3': None, 'Var_4': None}
                    for oVarCompCmp_STEP in sorted(oVarCompCmp_PAR.iteritems()):
                        oVarStats_PAR[oVarCompCmp_STEP[0]] = a1oFileStatsDyn_PAR[oVarCompCmp_STEP[1]]
                    # Get data
                    oVarData_PAR = a1oFileDataDyn_PAR[sFileDataDyn_PAR][sVarInfoDyn_CMP]
                    # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------
                    # Compute variable using analysis library
                    oVarDrv = Drv_Analysis_Cmp(Lib_Analysis_Cmp, sVarMethodCmp_PAR,
                                               a2dVarData=oVarData_PAR,
                                               a2dVarStDev=oVarStats_PAR['Var_1'],
                                               a2dVarMean=oVarStats_PAR['Var_2'],
                                               a2dModelStDev=oVarStats_PAR['Var_3'],
                                               a2dModelMean=oVarStats_PAR['Var_4'])

                    oVarMethod_Cmp = oVarDrv.get_func()
                    oVarArgs = oVarDrv.check_args(oVarMethod_Cmp)
                    a2dVar_CMP = oVarDrv.run_func(oVarMethod_Cmp, oVarArgs)

                    # Method to convert data from [%] to [-]
                    oVarMethod_Cnv = getattr(Lib_Var_Cnv, sVarMethodCnv_PAR)
                    a2dVar_CMP_FILTER = oVarMethod_Cnv(a2dVar_CMP, 1, 0)

                    # Debug
                    #plt.figure(1)
                    #plt.imshow(a2dVar_CMP); plt.colorbar(); plt.clim(0, 100);
                    #plt.figure(2)
                    #plt.imshow(a2dVar_CMP_FILTER); plt.colorbar(); plt.clim(0, 1);
                    #plt.show()
                    # -------------------------------------------------------------------------------------

                    # -------------------------------------------------------------------------------------
                    # Save results in a dictionary
                    a1oFileDataDyn_CMP[sVarInfoDyn_CMP] = {}
                    a1oFileDataDyn_CMP[sVarInfoDyn_CMP] = deepcopy(a2dVar_CMP_FILTER)
                    # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Info
            oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... OK ')
            # -------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_CMP = a1oFileDataDyn_CMP
            # -------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Pass variable to global workspace
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_CMP = {}
                oLogStream.info(
                    ' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data previously processed!')
            else:

                if not a1oFileDataDyn_PAR:
                    self.a1oFileDataDyn_CMP = {}
                    oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data not available!')
                if not a1oFileStatsDyn_PAR:
                    self.a1oFileDataDyn_CMP = {}
                    oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Stats not available!')

            # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # DEBUG START ###
        # import pickle
        # os.chdir(self.sPathClass)
        # oFile_CMP = open('oDataDyn_CMP_H16-SWI.pkl', 'wb')
        # pickle.dump(oVarSWI_CMP, oFile_CMP)
        # oFile_CMP.close()
        # import scipy.io as sio
        # os.chdir(self.sPathClass)
        # oData = {'SWI': oVarSWI_CMP}
        # sio.savemat('oDataDyn_CMP_H16-SWI.mat', oData)
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
                                                      'Satellite_HSAF-SWI-H16-STAR_FILENC_' + sTime_SAVE + '.history')

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

                # End if condition on file type format
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
