"""
Class Features

Name:          Cpl_Apps_Satellite_DynamicData_SoilMoisture_H16_Raw
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20161007'
Version:       '4.0.1'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os
import re
import datetime
import glob
import numpy as np

from os.path import join, split
from copy import deepcopy

import src.Lib_Analysis_Interpolation as Lib_Analysis
from src.Drv_Analysis_Interpolation import Drv_Analysis as Drv_Analysis

from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_File_Zip import Drv_File_Zip
from src.Drv_Exception import Exc

from src.Lib_File_Zip_Apps import removeFileUnzip, removeFileZip, checkFileNameZip
from src.Lib_File_Log_Apps import getFileHistory, writeFileHistory, checkSavingTime

from src.Lib_Op_System_Apps import deleteFileName, defineFileName, checkFileName, defineFolder
from src.Lib_Op_String_Apps import defineString
from src.Lib_Op_Dict_Apps import prepareDictKey, lookupDictKey
from src.Lib_Op_List_Apps import checkListAllSame

# Debug
#import matplotlib.pylab as plt
######################################################################################

# -------------------------------------------------------------------------------------
# Class
class Cpl_Apps_Satellite_DynamicData_HSAF_SoilMoisture_H16_Raw:

    # -------------------------------------------------------------------------------------
    # Class variable(s)
    oTags = None
    a1oFileDataDyn_CHK = None

    a1sFileDataDyn_SOURCE = None
    a1oVarsInfoDyn_SOURCE = None
    bData_SOURCE = False

    a1oFileDataDyn_GET = None
    a1oFileDataGeo_GET = None

    a1oFileDataDyn_PAR = None
    a1oVarsInfoDyn_PAR = None

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

    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to check data availability
    def checkDynamicData(self, sTime):
        
        #-------------------------------------------------------------------------------------
        # Info
        os.chdir(self.sPathSrc)
        sTime_CHK = sTime
        oLogStream.info(' ====> CHECK DATA AT TIME: ' + sTime_CHK + ' ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
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
        #-------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------
        # Condition to save file for reanalysis period
        bSaveTime_CHK = checkSavingTime(sTime_CHK, a1oTimeSteps_CHK, iTimeStep_CHK, iTimeUpd_CHK)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on file type
        a1sFileName_CHK = []
        a1bFileName_CHK = []
        a1sFileTime_CHK = []
        a1oFileDataDyn_CHK = {}
        for sFileType in oVarsWorkspace_CHK:
            
            #-------------------------------------------------------------------------------------
            # Check file type
            if sFileType == 'NetCDF':

                # Check file
                sFileCache_CHK = os.path.join(sPathCache_CHK, 'Satellite_HSAF-SM-H16-RAW_FILENC_' + sTime_CHK + '.history')
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
            
            # Debug ###
            #a1bFileName_CHK = []; a1bFileName_CHK.append(True)
            # #########
            
            # Saving results of checking file 
            a1oFileDataDyn_CHK = zip(a1sFileTime_CHK, a1sFileName_CHK, a1bFileName_CHK)
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Return check status 
        oLogStream.info(' ====> CHECK DATA AT TIME: ' + sTime + ' ... OK')
        # Return variable(s)
        self.a1oFileDataDyn_CHK = a1oFileDataDyn_CHK
        #------------------------------------------------------------------------------------
        
    #------------------------------------------------------------------------------------ 
    
    #------------------------------------------------------------------------------------- 
    # Method to retrieve data 
    def retrieveDynamicData(self, sTime):
        
        #-------------------------------------------------------------------------------------
        # Start message
        os.chdir(self.sPathSrc)
        sTime_RET = sTime
        oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get path informationLib_Analysis_Interpolation
        sPathDataDyn_SOURCE = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        # Get IN variable information
        oVarWorkspace_IN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        # Get check history 
        a1oFileDataDyn_CHK = self.a1oFileDataDyn_CHK 
        #-------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Check time steps selection
        if a1oFileDataDyn_CHK:

            #-------------------------------------------------------------------------------------
            # Checking time step data processing
            oTimeMatch = [iS for iS in a1oFileDataDyn_CHK if sTime_RET in iS]
            a1oTimeMatch = zip(*oTimeMatch)
            if a1oTimeMatch[2][0] is False:

                #-------------------------------------------------------------------------------------
                # Cycle(s) on file type(s)
                a1sFileDataDyn_SOURCE = []; a1oVarsInfoDyn_SOURCE = {}
                for sFileType in oVarWorkspace_IN:

                    # Get variable(s) information
                    oVarsInfo_IN = oVarWorkspace_IN[sFileType]

                    # Cycle(s) on variable(s)
                    for sVarType in oVarsInfo_IN:

                        # Get var information
                        oVarInfo_IN = oVarsInfo_IN[sVarType]

                        # Get variable(s) component(s)
                        oVarName_IN_LOADIN = oVarInfo_IN['VarOp']['Op_Load']['Comp']['IN']
                        oVarName_IN_LOADOUT = oVarInfo_IN['VarOp']['Op_Load']['Comp']['OUT']

                        oVarName_IN_MissValue = oVarInfo_IN['VarOp']['Op_Load']['Missing_value']
                        oVarName_IN_ValidRng = oVarInfo_IN['VarOp']['Op_Load']['Valid_range']
                        oVarName_IN_Zip = oVarInfo_IN['VarOp']['Op_Load']['Zip']

                        oVarMethodInterp_IN = oVarInfo_IN['VarOp']['Op_Math']['Interpolation']

                        # Get generic filename
                        sFileDataDyn_RAW = oVarInfo_IN['VarSource']

                        # File time period definition
                        iTimeDataDyn_SOURCE = int(oVarInfo_IN['VarTimeStep'])

                        # Get time information
                        oTime_RET_TO = datetime.datetime.strptime(sTime_RET,'%Y%m%d%H%M')
                        oTime_RET_FROM = oTime_RET_TO - datetime.timedelta(seconds=iTimeDataDyn_SOURCE)
                        sTime_RET_FROM = oTime_RET_FROM.strftime('%Y%m%d%H%M')
                        oTime_RET_TO = oTime_RET_TO - datetime.timedelta(seconds=1)
                        sTime_RET_TO = oTime_RET_TO.strftime('%Y%m%d%H%M')

                        # Define filename tags
                        sFileDataDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_RAW),
                                                                           {'$yyyy' : sTime_RET_TO[0:4],
                                                                            '$mm' : sTime_RET_TO[4:6],
                                                                            '$dd' : sTime_RET_TO[6:8],
                                                                            '$MM' : sTime_RET_TO[8:10],
                                                                            '$SS' : sTime_RET_TO[10:12]})

                        # Define filename with filepath
                        sFileDataDyn_TAGS = defineString(join(sPathDataDyn_SOURCE, sFileDataDyn_TAGS), self.oTags)
                        sFileDataDyn_TAGS = checkFileNameZip(sFileDataDyn_TAGS, oVarName_IN_Zip)
                        # Search all file(s) with selected root
                        a1sFileDataDyn_TAGS = sorted(glob.glob(sFileDataDyn_TAGS))

                        # Cycle(s) on filename tagged
                        for sFileDataDyn_TAGS in a1sFileDataDyn_TAGS:

                            # Match date in filename(s)
                            oMatch_TAGS = re.search(r'\d{4}\d{2}\d{2}\w\d{2}\d{2}', sFileDataDyn_TAGS)
                            if not oMatch_TAGS:
                                oMatch_TAGS = re.search(r'\d{4}\d{2}\d{2}\d{2}', sFileDataDyn_TAGS)
                            else:
                                pass

                            # Match date in filename(s)
                            #try:
                            #    oMatch_TAGS = re.search(r'\d{4}\d{2}\d{2}\w\d{2}\d{2}', sFileDataDyn_TAGS)  # yyyymmdd_HHMM
                            #except:
                            #    oMatch_TAGS = re.search(r'\d{4}\d{2}\d{2}\d{2}\d{2}', sFileDataDyn_TAGS)    # yyyymmddHHMM

                            # Get date of filename(s)
                            oMatch_Filter = re.compile(r"[^a-zA-Z0-9-]"); sTime_TAGS = oMatch_TAGS.group()
                            sTime_TAGS = oMatch_Filter.sub("",sTime_TAGS)
                            oTime_TAGS = datetime.datetime.strptime(sTime_TAGS[0:12], '%Y%m%d%H%M')

                            # Select data using time period
                            if (oTime_TAGS >= oTime_RET_FROM and oTime_TAGS < oTime_RET_TO):
                                a1sFileDataDyn_SOURCE.append(sFileDataDyn_TAGS)

                                if not sVarType in a1oVarsInfoDyn_SOURCE:
                                    a1oVarsInfoDyn_SOURCE[sVarType] = {}
                                    a1oVarsInfoDyn_SOURCE[sVarType]['Var_IN'] = oVarName_IN_LOADIN
                                    a1oVarsInfoDyn_SOURCE[sVarType]['Var_OUT'] = oVarName_IN_LOADOUT
                                    a1oVarsInfoDyn_SOURCE[sVarType]['Var_InterpMethod'] = oVarMethodInterp_IN
                                    a1oVarsInfoDyn_SOURCE[sVarType]['Var_MissingValue'] = oVarName_IN_MissValue
                                    a1oVarsInfoDyn_SOURCE[sVarType]['Var_ValidRange'] = oVarName_IN_ValidRng
                                    a1oVarsInfoDyn_SOURCE[sVarType]['Var_SaveMethod'] = ''
                                else:
                                    pass

                            else:
                                pass
                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Get list unique value(s)
                if a1sFileDataDyn_SOURCE:
                    a1sFileDataDyn_SOURCE = sorted(list(set(a1sFileDataDyn_SOURCE)))
                    # Exit message
                    oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... OK')
                    bData_SOURCE = True
                else:
                    a1sFileDataDyn_SOURCE = []; a1oVarsInfoDyn_SOURCE = {}
                    Exc.getExc(' -----> WARNING: no data selected in RETRIEVE DATA!', 2, 1)
                    # Exit message
                    oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... SKIPPED. Data not available!')
                    bData_SOURCE = False

                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Pass variable to global workspace
                self.a1sFileDataDyn_SOURCE = a1sFileDataDyn_SOURCE
                self.a1oVarsInfoDyn_SOURCE = a1oVarsInfoDyn_SOURCE
                self.bData_SOURCE = bData_SOURCE
                #-------------------------------------------------------------------------------------

            else:

                #-------------------------------------------------------------------------------------
                # Exit for previously processed data
                self.a1sFileDataDyn_SOURCE = []
                self.a1oVarsInfoDyn_SOURCE = {}
                self.bData_SOURCE = True
                oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... SKIPPED. Data previously processed!')
                #-------------------------------------------------------------------------------------

            #-------------------------------------------------------------------------------------

        else:

            # -------------------------------------------------------------------------------------
            # Exit for previously processed data
            self.a1sFileDataDyn_SOURCE = []
            self.a1oVarsInfoDyn_SOURCE = {}
            self.bData_SOURCE = True
            oLogStream.info(' ====> RETRIEVE DATA AT TIME: ' + sTime_RET + ' ... SKIPPED. No file(s) selected!')
            # -------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------  
    # Method to get data 
    def getDynamicData(self, sTime):
        
        #-------------------------------------------------------------------------------------
        # Info start
        os.chdir(self.sPathSrc)
        sTime_GET = sTime
        oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get information
        a1dGeoBox_REF = self.oDataGeo.a1dGeoBox
        a1sFileDataDyn_SOURCE = self.a1sFileDataDyn_SOURCE
        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE
        #-------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------
        # Check data workspace
        if a1oVarsInfoDyn_SOURCE:
            
            # Cycle(s) on selected file(s)
            a1oFileDataDyn_GET = {}
            a1oFileDataGeo_GET = {}
            for sFileDataDyn_GET in a1sFileDataDyn_SOURCE:

                # Info analyzed file
                oLogStream.info(' -----> FILE ANALYZED: ' + sFileDataDyn_GET)

                # Test file compression
                try:

                    # Unzip file
                    oZipDrv_GET = Drv_File_Zip(sFileDataDyn_GET, 'u', None, '.gz').oFileWorkspace
                    bFileZipCheck_GET = True    # no gz routine to test zip integrity

                    # Condition about file zip checking
                    if bFileZipCheck_GET:
                        [oFile_GET_IN, oFile_GET_OUT] = oZipDrv_GET.oFileLibrary.openZip(oZipDrv_GET.sFileName_IN,
                                                                                         oZipDrv_GET.sFileName_OUT,
                                                                                         oZipDrv_GET.sZipMode)
                        oZipDrv_GET.oFileLibrary.unzipFile(oFile_GET_IN, oFile_GET_OUT)
                        oZipDrv_GET.oFileLibrary.closeZip(oFile_GET_IN, oFile_GET_OUT)

                        # Open file after unzipping
                        oDrvData_GET = Drv_Data_IO(oZipDrv_GET.sFileName_OUT).oFileWorkspace
                        oFile_GET = oDrvData_GET.oFileLibrary.openFile(oZipDrv_GET.sFileName_OUT)

                    else:
                        pass

                except:

                    # Open file
                    oDrvData_GET = Drv_Data_IO(sFileDataDyn_GET).oFileWorkspace
                    oFile_GET = oDrvData_GET.oFileLibrary.openFile(sFileDataDyn_GET)

                # Cycle(s) on variable(s)
                a1oFileDataDyn_TEST = {}
                a1oFileDataDyn_GET[sFileDataDyn_GET] = {}
                a1oFileDataGeo_GET[sFileDataDyn_GET] = {}
                for sVarNameDyn_SOURCE in a1oVarsInfoDyn_SOURCE:

                    # Get variable information
                    oVarInfoDyn_GET_IN = prepareDictKey([sVarNameDyn_SOURCE, 'Var_IN', 'Var_1'])
                    sVarNameDyn_GET_IN = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_GET_IN)

                    oVarInfoDyn_GET_OUT = prepareDictKey([sVarNameDyn_SOURCE, 'Var_OUT', 'Var_1'])
                    sVarNameDyn_GET_OUT = lookupDictKey(a1oVarsInfoDyn_SOURCE, *oVarInfoDyn_GET_OUT)

                    # Read data information
                    a2dVar_GET = oDrvData_GET.oFileLibrary.readData(oFile_GET, sVarNameDyn_GET_IN)

                    # Check data availability in array variable
                    if a2dVar_GET.size:

                        # Save variable data into workspace
                        if not sVarNameDyn_SOURCE == 'Longitude' and not sVarNameDyn_SOURCE == 'Latitude':
                            try:
                                a1oFileDataDyn_GET[sFileDataDyn_GET][sVarNameDyn_GET_IN] = {}
                                a1oFileDataDyn_GET[sFileDataDyn_GET][sVarNameDyn_GET_IN] = a2dVar_GET
                                a1oFileDataDyn_TEST[sVarNameDyn_SOURCE] = a2dVar_GET
                            except:
                                a1oFileDataDyn_GET[sFileDataDyn_GET][sVarNameDyn_GET_IN] = None
                                a1oFileDataDyn_TEST[sVarNameDyn_SOURCE] = None
                        else:
                            pass

                        # Save geographical information into workspace
                        if (sVarNameDyn_SOURCE == 'Longitude') and ('Longitude' not in a1oFileDataGeo_GET[sFileDataDyn_GET]):
                            try:
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Longitude'] = a2dVar_GET
                                a1oFileDataDyn_TEST['Longitude'] = a2dVar_GET
                            except:
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Longitude'] = None
                                a1oFileDataDyn_TEST['Longitude'] = None

                        else:
                            pass
                        if (sVarNameDyn_SOURCE == 'Latitude') and ('Latitude' not in a1oFileDataGeo_GET[sFileDataDyn_GET]):
                            try:
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Latitude'] = a2dVar_GET
                                a1oFileDataDyn_TEST['Latitude'] = a2dVar_GET
                            except:
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Latitude'] = None
                                a1oFileDataDyn_TEST['Latitude'] = None
                        else:
                            pass

                    else:
                        pass

                    # Rewind bufr file at beginning
                    oFile_GET = oDrvData_GET.oFileLibrary.rewindFile(oFile_GET)

                # Close file bufr
                oDrvData_GET.oFileLibrary.closeFile(oFile_GET)
                #-------------------------------------------------------------------------------------

                # -------------------------------------------------------------------------------------
                # Check variable(s) dimension(s)
                a1oVarDim_TEST = []
                if a1oFileDataDyn_TEST:
                    for sVarNameDyn_TEST in a1oFileDataDyn_TEST:
                        try:
                            a2dVarData_TEST = a1oFileDataDyn_TEST[sVarNameDyn_TEST]
                            iVarDim_TEST = a2dVarData_TEST.shape[0]
                            a1oVarDim_TEST.append(iVarDim_TEST)
                        except:
                            a1oVarDim_TEST.append(-1)
                else:
                    a1oVarDim_TEST = None
                bCheckDim_TEST = checkListAllSame(a1oVarDim_TEST)
                # -------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Check variable(s) dimension(s)
                if bCheckDim_TEST:

                    # Check data geographical limits with reference limits
                    if ('Latitude' in a1oFileDataGeo_GET[sFileDataDyn_GET] and
                       'Longitude' in a1oFileDataGeo_GET[sFileDataDyn_GET]):

                        # Get geographical information
                        a1dGeoY_GET = a1oFileDataGeo_GET[sFileDataDyn_GET]['Latitude']
                        a1dGeoX_GET = a1oFileDataGeo_GET[sFileDataDyn_GET]['Longitude']

                        if not (a1dGeoX_GET == None) and not (a1dGeoX_GET == None):

                            a1iIndex_GET = []
                            if a1dGeoY_GET.shape[0] == a1dGeoX_GET.shape[0]:
                                a1iIndex_GET = np.nonzero(((a1dGeoX_GET >= a1dGeoBox_REF[0]) & (a1dGeoX_GET <= a1dGeoBox_REF[2])) &
                                                          ((a1dGeoY_GET >= a1dGeoBox_REF[3]) & (a1dGeoY_GET <= a1dGeoBox_REF[1])))

                                a1iIndex_GET = a1iIndex_GET[0]
                            else:
                                pass

                            # Check geographical box ref with geographical information
                            if any(a1iIndex_GET):
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Index'] = {}
                                a1oFileDataGeo_GET[sFileDataDyn_GET]['Index'] = a1iIndex_GET
                            else:
                                # Delete key(s) that not matching with box limit(s)
                                a1oFileDataDyn_GET.pop(sFileDataDyn_GET, None)
                                a1oFileDataGeo_GET.pop(sFileDataDyn_GET, None)

                        else:
                            # Delete key(s) if longitude or latitude are not defined
                            a1oFileDataDyn_GET.pop(sFileDataDyn_GET, None)

                    else:
                        # Delete key(s) if longitude or latitude are not defined
                        a1oFileDataDyn_GET.pop(sFileDataDyn_GET, None)

                else:
                    # Delete key(s) that not matching for dimensions
                    a1oFileDataDyn_GET.pop(sFileDataDyn_GET, None)
                    a1oFileDataGeo_GET.pop(sFileDataDyn_GET, None)
                    Exc.getExc(' -----> WARNING: variables dimension are not all the same!', 2, 1)
                # -------------------------------------------------------------------------------------

            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Info end
            oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... OK ')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_GET = a1oFileDataDyn_GET
            self.a1oFileDataGeo_GET = a1oFileDataGeo_GET
            #-------------------------------------------------------------------------------------
            
        else:
            
            #-------------------------------------------------------------------------------------
            # Exit for previously processed data
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_GET = {}
                self.a1oFileDataGeo_GET = {}
                oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_GET = {}
                self.a1oFileDataGeo_GET = {}
                oLogStream.info(' ====> GET DATA AT TIME: ' + sTime_GET + ' ... SKIPPED. Data not available!')
            #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        
        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_GET = open('oDataDyn_GET.pkl', 'wb')
        #pickle.dump(a1oFileDataDyn_GET, oData_GET)
        #oData_GET.close()
        #oGeo_GET = open('oDataGeo_GET.pkl', 'wb')
        #pickle.dump(a1oFileDataGeo_GET, oGeo_GET)
        #oGeo_GET.close()
        # DEBUG END #####
         
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------
    # Method to parser data 
    def parserDynamicData(self, sTime):
        
        # DEBUG START ###
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_GET = open('oDataDyn_GET.pkl', 'rb')
        #a1oFileDataDyn_GET = pickle.load(oData_GET)
        #oData_GET.close()
        #oGeo_GET = open('oDataGeo_GET.pkl', 'rb')
        #a1oFileDataGeo_GET = pickle.load(oGeo_GET)
        #oGeo_GET.close()
        #self.a1oFileDataDyn_GET = a1oFileDataDyn_GET
        #self.a1oFileDataGeo_GET = a1oFileDataGeo_GET
        # DEBUG END #####
        
        #------------------------------------------------------------------------------------- 
        # Info
        os.chdir(self.sPathSrc)
        sTime_PAR = sTime
        oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... ')
        #------------------------------------------------------------------------------------- 

        #-------------------------------------------------------------------------------------
        # Get information
        sPathTemp = self.oDataInfo.oInfoSettings.oPathInfo['DataTemp']
        
        oDataGeo = self.oDataGeo
        
        a1oVarsInfoDyn_SOURCE = self.a1oVarsInfoDyn_SOURCE
        a1oFileDataDyn_GET = self.a1oFileDataDyn_GET
        a1oFileDataGeo_GET = self.a1oFileDataGeo_GET
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Check data workspace
        if a1oFileDataDyn_GET: 
            
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

                        # Condition to avoid geographical information in source variable(s)
                        if sVarName_SOURCE != 'Longitude' and sVarName_SOURCE != 'Latitude':

                            # Condition to avoid geographical information in parser variable(s)
                            sVarName_PAR = oVarName_PAR.values()[0]
                            if sVarName_PAR != 'Longitude' and sVarName_PAR != 'Latitude':

                                # Check variable availability in data file
                                if sVarName_SOURCE in oFileDataDyn_GET:

                                    # Get interpolation method
                                    sVarMethodInterp_SOURCE = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_InterpMethod']['Func']

                                    # Get interpolatation setting(s)
                                    dVar_XRad_SOURCE = float(a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_InterpMethod']['XRad'])
                                    dVar_YRad_SOURCE = float(a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_InterpMethod']['YRad'])

                                    # Get var limit(s) and undefined value
                                    dVar_MissValue_SOURCE = float(a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_MissingValue'])
                                    oVar_ValidRange_SOURCE = a1oVarsInfoDyn_SOURCE[sVarInfoDyn_SOURCE]['Var_ValidRange']
                                    a1dVar_ValidRange_SOURCE = np.asarray(oVar_ValidRange_SOURCE.split(','))

                                    # Get data values
                                    oVar_GET = oFileDataDyn_GET[sVarName_SOURCE]

                                    oVarDrv = Drv_Analysis(Lib_Analysis, sVarMethodInterp_SOURCE,
                                                           oGeoX_OUT=oDataGeo.a2dGeoX, oGeoY_OUT=oDataGeo.a2dGeoY,
                                                           oGeoNan_OUT=oDataGeo.a2bGeoDataNaN,
                                                           oData_IN=oVar_GET,
                                                           oGeoX_IN=oFileDataGeo_GET['Longitude'],
                                                           oGeoY_IN=oFileDataGeo_GET['Latitude'],
                                                           dRadiusX_OUT=dVar_XRad_SOURCE,
                                                           dRadiusY_OUT=dVar_YRad_SOURCE,
                                                           sPathTemp=sPathTemp)

                                    oVarMethod = oVarDrv.get_func()
                                    oVarArgs = oVarDrv.check_args(oVarMethod)
                                    a2dVar_INTERP = oVarDrv.run_func(oVarMethod, oVarArgs)

                                    try:
                                        a2dVar_INTERP[np.isnan(a2dVar_INTERP)] = np.nan
                                        a2dVar_INTERP[a2dVar_INTERP < float(a1dVar_ValidRange_SOURCE[0])] = np.nan
                                        a2dVar_INTERP[a2dVar_INTERP > float(a1dVar_ValidRange_SOURCE[1])] = np.nan

                                    except:
                                        pass

                                    # Filter data using geographical mask
                                    a2dVar_INTERP[oDataGeo.a2bGeoDataNaN] = np.nan

                                    # Debug ####
                                    #plt.figure(1)
                                    #plt.imshow(a2dVar_INTERP); plt.colorbar(); plt.clim(0, 100);
                                    #plt.show()
                                    ############

                                    # Store data in interpolated variable(s) workspace
                                    a1oFileDataDyn_PAR[sFileDataDyn_GET][sVarName_PAR] = {}
                                    a1oFileDataDyn_PAR[sFileDataDyn_GET][sVarName_PAR] = a2dVar_INTERP

                                    if not sVarInfoDyn_SOURCE in a1oVarsInfoDyn_PAR:
                                        a1oVarsInfoDyn_PAR[sVarInfoDyn_SOURCE] = {}
                                        a1oVarsInfoDyn_PAR[sVarInfoDyn_SOURCE] = sVarName_PAR
                                    else:
                                        pass

                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
            #-------------------------------------------------------------------------------------            

            #-------------------------------------------------------------------------------------
            # Info end
            oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... OK ')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_PAR = a1oFileDataDyn_PAR
            self.a1oVarsInfoDyn_PAR = a1oVarsInfoDyn_PAR
            #-------------------------------------------------------------------------------------
        
        else:
            
            #-------------------------------------------------------------------------------------
            # Pass variable to global workspace
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_PAR = {}
                self.a1oVarsInfoDyn_PAR = {}
                oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_PAR = {}
                self.a1oVarsInfoDyn_PAR = {}
                oLogStream.info(' ====> PARSER DATA AT TIME: ' + sTime_PAR + ' ... SKIPPED. Data not available!')
            #-------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # DEBUG START ####################################################################
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_PAR_1 = open('oData_PAR_H07.pkl', 'wb')
        #pickle.dump(a1oFileDataDyn_PAR, oData_PAR_1)
        #oData_PAR_1.close()
        #oData_PAR_2 = open('oVars_PAR_H07.pkl', 'wb')
        #pickle.dump(a1oVarsInfoDyn_PAR, oData_PAR_2)
        #oData_PAR_2.close()
        # DEBUG END ######################################################################

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to compute data 
    def computeDynamicData(self, sTime):

        # DEBUG START ####################################################################
        #import pickle
        #os.chdir(self.sPathClass)
        #oData_PAR_1 = open('oData_PAR_H07.pkl', 'rb')
        #a1oFileDataDyn_PAR = pickle.load(oData_PAR_1)
        #oData_PAR_1.close()
        #oData_PAR_2 = open('oVars_PAR_H07.pkl', 'rb')
        #a1oVarsInfoDyn_PAR = pickle.load(oData_PAR_2)
        #oData_PAR_2.close()
        #self.a1oFileDataDyn_PAR = a1oFileDataDyn_PAR
        #self.a1oVarsInfoDyn_PAR = a1oVarsInfoDyn_PAR
        # DEBUG END ######################################################################

        #------------------------------------------------------------------------------------- 
        # Info
        os.chdir(self.sPathSrc)
        sTime_CMP = sTime
        oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... ')
        #------------------------------------------------------------------------------------- 
        
        #-------------------------------------------------------------------------------------
        # Get information
        a1oFileDataDyn_PAR = self.a1oFileDataDyn_PAR 
        a1oVarsInfoDyn_PAR = self.a1oVarsInfoDyn_PAR 
        
        oDataGeo = self.oDataGeo
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Check data workspace
        if a1oFileDataDyn_PAR and a1oVarsInfoDyn_PAR:
            
            # Cycle(s) on variable(s)
            a1oFileDataDyn_CMP = {}
            a2dVarData_CMP = np.zeros([oDataGeo.iRows, oDataGeo.iCols])
            a2dVarData_CMP[:, :] = np.nan
            a2dVarIndex_CMP = np.zeros([oDataGeo.iRows, oDataGeo.iCols])
            a2dVarIndex_CMP[:, :] = np.nan
            for sVarsKeysDyn_PAR, sVarsValueDyn_PAR in a1oVarsInfoDyn_PAR.iteritems():
                
                # Cycle(s) on filename(s)
                a1oFileNameDyn_CMP = {}
                for iFileDataDyn_PAR, sFileDataDyn_PAR in enumerate(a1oFileDataDyn_PAR):

                    # Count file selected in for cycle(s) (adding to avoid 0 value)
                    iFileDataDyn_PAR_COUNT = iFileDataDyn_PAR + 1
                    # Raw variable
                    a2dVarData_PAR = np.zeros([oDataGeo.iRows, oDataGeo.iCols]); a2dVarData_PAR[:, :] = np.nan
                    a2dVarData_PAR = a1oFileDataDyn_PAR[sFileDataDyn_PAR][sVarsValueDyn_PAR]
                    # Get not finite indexes
                    a2iVarIndex_PAR = np.where(np.isfinite(a2dVarData_PAR))

                    # Update variable
                    a2dVarData_CMP[a2iVarIndex_PAR[0], a2iVarIndex_PAR[1]] = a2dVarData_PAR[a2iVarIndex_PAR[0], a2iVarIndex_PAR[1]]
                    a2dVarIndex_CMP[a2iVarIndex_PAR[0], a2iVarIndex_PAR[1]] = iFileDataDyn_PAR_COUNT

                    # Update filename
                    a1oFileNameDyn_CMP[iFileDataDyn_PAR_COUNT] = {}
                    a1oFileNameDyn_CMP[iFileDataDyn_PAR_COUNT] = split(sFileDataDyn_PAR)[1]
                    
                    # Debug ###
                    #a2dVarData_PAR[a2dVarData_PAR<0] = np.nan
                    #plt.figure(1)
                    #plt.imshow(a2dVarData_PAR); plt.colorbar(); plt.clim(0, 100)
                    #plt.figure(2)
                    #plt.imshow(a2dVarData_CMP); plt.colorbar(); plt.clim(0, 100)
                    #plt.show()
                    # #########

                # Copy array to avoid variable overriding
                a2dVarData_CMP_FINAL = deepcopy(a2dVarData_CMP)

                # Put data in a workspace
                if not sVarsKeysDyn_PAR in a1oFileDataDyn_CMP:
                    a1oFileDataDyn_CMP[sVarsKeysDyn_PAR] = {}
                    a1oFileDataDyn_CMP[sVarsKeysDyn_PAR] = a2dVarData_CMP_FINAL
                else:
                    pass
                if not 'SM_FileIndex' in a1oFileDataDyn_CMP:
                    a1oFileDataDyn_CMP['SM_FileIndex'] = {}
                    a1oFileDataDyn_CMP['SM_FileIndex'] = a2dVarIndex_CMP
                else:
                    pass
                if not 'SM_FileName' in a1oFileDataDyn_CMP:
                    a1oFileDataDyn_CMP['SM_FileName'] = {}
                    a1oFileDataDyn_CMP['SM_FileName'] = a1oFileNameDyn_CMP
                else:
                    pass

            # Debug ###
            #plt.figure(1)
            #plt.imshow(a1oFileDataDyn_CMP[sVarsKeysDyn_PAR]); plt.clim(0, 100)
            #plt.colorbar()
            #plt.figure(2)
            #plt.imshow(a1oFileDataDyn_CMP['SM_FileIndex']); plt.clim(0, 10)
            #plt.colorbar()
            #plt.show()
            # #########

            #------------------------------------------------------------------------------------- 

            #------------------------------------------------------------------------------------- 
            # Info
            oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... OK ')
            #------------------------------------------------------------------------------------- 
            
            #-------------------------------------------------------------------------------------
            # Pass variable to global workspace
            self.a1oFileDataDyn_CMP = a1oFileDataDyn_CMP
            #-------------------------------------------------------------------------------------

        else:
            
            #-------------------------------------------------------------------------------------
            # Pass variable to global workspace
            if self.bData_SOURCE is True:
                self.a1oFileDataDyn_CMP = {}
                oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data previously processed!')
            else:
                self.a1oFileDataDyn_CMP = {}
                oLogStream.info(' ====> COMPUTE DATA AT TIME: ' + sTime_CMP + ' ... SKIPPED. Data not available!!')
            #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------------------
    # Method to save data
    def saveDynamicData(self, sTime):
        
        # -------------------------------------------------------------------------------------
        # Info
        os.chdir(self.sPathSrc)
        sTime_SAVE = sTime
        oLogStream.info(' ====> SAVE DATA AT TIME: ' + sTime_SAVE + ' ...  ')
        # -------------------------------------------------------------------------------------
        
        # -------------------------------------------------------------------------------------
        # Get information
        a1oFileDataDyn_CMP = self.a1oFileDataDyn_CMP
        a1oVarsInfoDyn_PAR = self.a1oVarsInfoDyn_PAR

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
                    # Cycle(s) on variable(s)
                    for sVarKeys_OUT, sVarName_OUT in a1oVarsInfoDyn_PAR.iteritems():

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
                        sFileNameDyn_OUT = defineFileName(join(sPathDataDyn_OUT, oVarsInfo_OUT[sVarName_OUT]['VarSource']),
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
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeFileAttrsCommon(oFileData_OUT,
                                                                                                        self.oDataInfo.oInfoSettings.oGeneralInfo,
                                                                                                        split(sFileNameDyn_OUT)[0])
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeFileAttrsExtra(oFileData_OUT,
                                                                                                       self.oDataInfo.oInfoSettings.oParamsInfo,
                                                                                                       self.oDataGeo.a1oGeoHeader)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeFileAttrsArray(oFileData_OUT,
                                                                                                       'FileName',
                                                                                                       a1oFileDataDyn_CMP['SM_FileName'])
                                # -------------------------------------------------------------------------------------
                                
                                # -------------------------------------------------------------------------------------
                                # Write geo-system information
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeGeoSystem(oFileData_OUT,
                                                                                                  self.oDataInfo.oInfoSettings.oGeoSystemInfo, 
                                                                                                  self.oDataGeo.a1dGeoBox)
                                # -------------------------------------------------------------------------------------
                                
                                # -------------------------------------------------------------------------------------
                                # Declare variable dimensions
                                sDimVarX = oVarsInfo_OUT['Terrain']['VarDims']['X']
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT, sDimVarX, self.oDataGeo.iCols)
                                sDimVarY = oVarsInfo_OUT['Terrain']['VarDims']['Y']
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT, sDimVarY, self.oDataGeo.iRows)
                                sDimVarT = 'time'
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT, sDimVarT, iVarLen_OUT)
                                # Declare extra dimension(s)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT, 'nsim', 1)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT, 'ntime', 2)
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeDims(oFileData_OUT, 'nens', 1)
                                # -------------------------------------------------------------------------------------
                                
                                # -------------------------------------------------------------------------------------
                                # Write time information
                                oFileDrv_OUT.oFileData = oFileDrv_OUT.oFileLibrary.writeTime(oFileData_OUT,
                                                                                             a1oVarTime_OUT, 'f8', 'time', 
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
                                    oLogStream.info(' -------> Saving variable: ' + sVarGeoX + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE')
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
                                    oLogStream.info(' -------> Saving variable: ' + sVarGeoY + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE')
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
                                                                   oVarsInfo_OUT[sVarTerrain]['VarOp']['Op_Save']['Func'])
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
                                    oLogStream.info(' -------> Saving variable: ' + sVarTerrain + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE')
                                    # -------------------------------------------------------------------------------------
                                
                                # -------------------------------------------------------------------------------------
                                
                                # -------------------------------------------------------------------------------------
                                # Try to save index
                                sVarIndex = 'SM_FileIndex'
                                a2dIndex = a1oFileDataDyn_CMP[sVarIndex]
                                a2dIndex[self.oDataGeo.a2bGeoDataNaN] = float(oVarsInfo_OUT[sVarIndex]['VarOp']['Op_Save']['Missing_value'])
                                a2dIndex[np.isnan(a2dIndex)] = float(oVarsInfo_OUT[sVarIndex]['VarOp']['Op_Save']['Missing_value'])
                                
                                oLogStream.info(' -------> Saving variable: ' + sVarIndex + ' ... ')
                                try:                     
                                
                                    # -------------------------------------------------------------------------------------
                                    # Get terrain  
                                    oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary,  
                                                                   oVarsInfo_OUT[sVarIndex]['VarOp']['Op_Save']['Func'])
                                    oFileDRV_WriteMethod(oFileData_OUT,
                                                         sVarIndex, a2dIndex, 
                                                         oVarsInfo_OUT[sVarIndex]['VarAttributes'], 
                                                         oVarsInfo_OUT[sVarIndex]['VarOp']['Op_Save']['Format'], 
                                                         oVarsInfo_OUT[sVarIndex]['VarDims']['Y'], 
                                                         oVarsInfo_OUT[sVarIndex]['VarDims']['X'])
                                    # Info
                                    a1bFileCheck_HIS.append(True)
                                    oLogStream.info(' -------> Saving variable: ' + sVarIndex + ' ... OK ')
                                    # -------------------------------------------------------------------------------------
                            
                                except:
                                    
                                    # -------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileCheck_HIS.append(False)
                                    Exc.getExc(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info(' -------> Saving variable: ' + sVarIndex + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE')
                                    # -------------------------------------------------------------------------------------
                                
                                # -------------------------------------------------------------------------------------
                                
                                # -------------------------------------------------------------------------------------
                                # Try to save 2d/3d variable
                                oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... ')
                                
                                a2VarData_OUT = a1oFileDataDyn_CMP[sVarName_OUT]
                                a2VarData_OUT[self.oDataGeo.a2bGeoDataNaN] = float(oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])
                                a2VarData_OUT[np.isnan(a2VarData_OUT)] = float(oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])

                                try:
                                
                                    # -------------------------------------------------------------------------------------
                                    # Get data dynamic
                                    oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary, 
                                                                 oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Func'])
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
                                    oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE')
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
                                a1sFileName_HIS.append(sFileNameDyn_OUT + '.' + oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Zip'])
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
                                    a2VarData_OUT[self.oDataGeo.a2bGeoDataNaN] = float(oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])
                                    a2VarData_OUT[np.isnan(a2VarData_OUT)] = float(oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Missing_value'])
                                    try:
                                    
                                        # -------------------------------------------------------------------------------------
                                        # Get data dynamic
                                        oFileDRV_WriteMethod = getattr(oFileDrv_OUT.oFileLibrary, 
                                                                       oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Func'])
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
                                        oLogStream.info(' -------> Saving variable: ' + sVarName_OUT + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE')
                                        # -------------------------------------------------------------------------------------
                                    
                                    # -------------------------------------------------------------------------------------
                                
                                else:

                                    # -------------------------------------------------------------------------------------
                                    # Info
                                    oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... SAVED PREVIOUSLY')
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
                                a1sFileName_HIS.append(sFileNameDyn_OUT + '.' + oVarsInfo_OUT[sVarName_OUT]['VarOp']['Op_Save']['Zip'])
                                oLogStream.info(' ------> Saving file output NetCDF: ' + sFileNameDyn_OUT + ' ... OK')
                                # -------------------------------------------------------------------------------------
                                
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
                        sFileCache_HIS = os.path.join(sPathCache_HIS, 'Satellite_HSAF-SM-H16-RAW_FILENC_' + sTime_SAVE + '.history')
                        
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
                    oLogStream.info(' ====> SAVE DATA AT TIME: ' + sTime_SAVE + ' ...  SKIPPED. Format data output UNKNOWN')
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
