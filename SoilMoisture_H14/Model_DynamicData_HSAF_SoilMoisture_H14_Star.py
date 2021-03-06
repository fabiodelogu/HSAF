#-------------------------------------------------------------------------------------
# HSAF - Data Dynamic SoilMoisture H14 Star
# Version 4.0.0 (20161005)
#
# Author(s):    Fabio Delogu        (fabio.delogu@cimafoundation.org)
#               Simone Gabellani    (simone.gabellani@cimafoundation.org)
#
# Python 2.7
#
# References external libraries:
# numpy-scipy:        http://www.scipy.org/SciPy
# python-netcdf:      http://netcdf4-python.googlecode.com/svn/trunk/docs/netCDF4-module.html
# python-gdal:        https://pypi.python.org/pypi/GDAL/
#
# Function Argument(s): -settingfile -logfile
#
# Function returns:
# iExitStatus             Function code error
#                          0: OK
#                          1: Error in "Set algorithm"
#                          2: Error in "Initialize algorithm"
#                          3: Error in "Execute algorithm"
#
# Example: 
# python Model_DynamicData_HSAF_SoilMoisture_H14_Star.py -settingfile settingfile.config -logfile logfile.config
#
# General example usage:
# python Model_DynamicData_HSAF_SoilMoisture_H14_Star.py
# -settingfile /home/fabio/Documents/Working_Area/Code_Development/Workspace/Liclipse_Workspace/Project_HSAF/Product_SoilMoisture_2016/config_algorithm/model_dynamicdata_hsaf-sm-h14-star_algorithm_server_history.config
# -logfile /home/fabio/Documents/Working_Area/Code_Development/Workspace/Liclipse_Workspace/Project_HSAF/Product_SoilMoisture_2016/config_logs/model_dynamicdata_hsaf-sm-h14-star_logging_server_history.config
#
# Versions:
# 20161005 (4.0.0) --> First release 4.0.0
# 20140708 (3.0.8) --> Last release based on previously H07 and H14 script(s) versions 1-2-3 
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Method to get script argument(s)
def GetArgs():
    
    import argparse

    oParser = argparse.ArgumentParser()
    oParser.add_argument('-settingfile', action="store", dest="sSettingFile")
    oParser.add_argument('-logfile', action="store", dest="sLoggingFile")
    oParserValue = oParser.parse_args()
    
    sScriptName = oParser.prog
    
    if oParserValue.sSettingFile:
        sSettingsFile = oParserValue.sSettingFile
    else:
        sSettingsFile = 'model_dynamicdata_hsaf-sm-h14-star_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'model_dynamicdata_hsaf-sm-h14-star_logging.config'
    
    return sScriptName, sSettingsFile, sLoggingFile

#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #-------------------------------------------------------------------------------------
    # Versio
    sProgramVersion = '4.0.0'
    sProjectName = 'Model'
    sAlgName = 'HSAF SM H14 STAR'
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Get script argument(s)
    [sScriptName, sSettingsFile, sLoggingFile] = GetArgs()
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Log initialization
    import logging
    import logging.config
    logging.config.fileConfig(sLoggingFile)
    oLogStream = logging.getLogger('sLogger')
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Start Program
    oLogStream.info('[' + sProjectName + ' DataDynamic - ' + sAlgName + ' (Version ' + sProgramVersion + ')]')
    oLogStream.info('[' + sProjectName + '] Start Program ... ')
    iExitStatus = 0
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Load LandData setting(s)
    oLogStream.info('[' + sProjectName + '] DataDynamic - Load ' + sAlgName + ' configuration ... ')
    
    # Check section
    try:
    
        #-------------------------------------------------------------------------------------
        # Complete library
        import os
        import time
    
        # Partial library
        from sys import argv
        from os.path import join
        from os.path import abspath
        
        # Import classes
        from src.Drv_Exception import Exc
        from src.Drv_Settings import Settings
        from src.Drv_Time import Time
        from src.Drv_Data_Geo import DataGeo
        from src.Drv_Data_Ancillary_HSAF_SoilMoisture import DataAncillary
        
        from Cpl_Apps_Model_DynamicData_HSAF_SoilMoisture_H14_Star import Cpl_Apps_Model_DynamicData_HSAF_SoilMoisture_H14_Star
        
        # Debugging library
        # import matplotlib.pylab as plt
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Path main
        sPathMain = os.getcwd() + '/'  # Setting PathMain
        abspath(sPathMain)  # Entering in path main folder
        #-------------------------------------------------------------------------------------
    
        #-------------------------------------------------------------------------------------
        # Get information data
        oDataInfo = Settings(sSettingsFile).getSettings()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Time information
        dStartTime = time.time()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DataDynamic - Load ' + sAlgName + ' configuration ... OK')
        #-------------------------------------------------------------------------------------
        
    except:
    
        #-------------------------------------------------------------------------------------
        # Algorithm exception(s)
        Exc.getExc('[' + sProjectName + '] DataDynamic - Load ' + sAlgName + ' configuration ... FAILED', 1, 1)
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] DataDynamic - Initialize ' + sAlgName + ' ... ')
    
    # Check section
    try:
        
        #-------------------------------------------------------------------------------------
        # Get terrain data
        oDataTerrain = DataGeo(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'],
                               oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource'])).getDataGeo()

        # Get statistics data - H14
        oDataStats = DataAncillary(
            sFileName=join(oDataInfo.oInfoSettings.oPathInfo['DataAncillary'],
                           oDataInfo.oInfoVarStatic.oDataInputStatic['NetCDF']['SM_Statistics']['VarSource']),
            sDataName='SM_Statistics',
            sTimeNow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow']).getData()

        # Get time data
        oDataTime = Time(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'],
                         timedelta=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                         timesteppast=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriod']),
                         timerefHH=['00'],
                         timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef']).getTime()
        #-------------------------------------------------------------------------------------
    
        #-------------------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DataDynamic - Initialize HSAF SWI H16 ... OK')
        #-------------------------------------------------------------------------------------
    
    except:
    
        #-------------------------------------------------------------------------------------
        # Algorithm exception(s)
        Exc.getExc('[' + sProjectName + '] DataDynamic - Initialize ' + sAlgName + ' ... FAILED', 1, 2)
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] DataDynamic - Execute ' + sAlgName + ' ... ')
    
    # Check section
    try:
        
        #-------------------------------------------------------------------------------------
        # Dynamic Data
        oCpl_DynamicData = Cpl_Apps_Model_DynamicData_HSAF_SoilMoisture_H14_Star(oDataTime=oDataTime, oDataGeo=oDataTerrain,
                                                                                 oDataAncillary=oDataStats, oDataInfo=oDataInfo)
        
        # Cycle on time steps
        for sTime in oDataTime.a1oTimeSteps:
            
            # Define Tags
            oCpl_DynamicData.defineDynamicTags(sTime)

            # Check dynamic data availability
            oCpl_DynamicData.checkDynamicData(sTime)
            
            # Check dynamic data availability
            oCpl_DynamicData.retrieveDynamicData(sTime)
            
            # Get dynamic data
            oCpl_DynamicData.getDynamicData(sTime)
            
            # Parser dynamic data
            oCpl_DynamicData.parserDynamicData(sTime)
            
            # Compute dynamic data
            oCpl_DynamicData.computeDynamicData(sTime)
            
            # Save dynamic data
            oCpl_DynamicData.saveDynamicData(sTime)
            
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DataDynamic - Execute ' + sAlgName + ' ... OK')
        #-------------------------------------------------------------------------------------
    
    except:
    
        #-------------------------------------------------------------------------------------
        # Algorithm exception(s)
        Exc.getExc('[' + sProjectName + '] DataDynamic - Execute ' + sAlgName + ' ... FAILED', 1, 3)
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Note about script parameter(s)
    oLogStream.info('NOTE - Algorithm parameter(s)')
    oLogStream.info('Script: ' + str(sScriptName))
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # End Program
    dTimeElapsed = round(time.time() - dStartTime, 1)
    
    oLogStream.info('[' + sProjectName + '] DataDynamic - ' + sAlgName + ' (Version ' + sProgramVersion + ')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')

    Exc.getExc('', 0, 0)
    #-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
