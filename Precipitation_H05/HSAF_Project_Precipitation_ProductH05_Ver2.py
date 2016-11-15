#----------------------------------------------------------------------------
"""
Project HSAF - PRECIPITATION PRODUCT H05

__date__ = '20141204'
__version__ = '2.0.0'
__author__ = 'Fabio Delogu'
__library__ = 'hdf5 grib'

General command line:
python HSAF_Project_Precipitation_ProductH05_VerX.py settings_precipitation_product_h05.txt

Version:
20141204 (2.0.0) --> New release starting from Ver. 1

"""
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Versioning
sProgramVersion = '2.0.0'
sProjectName = 'PROJECT HSAF'
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Start Program
print('[' + sProjectName + '] - PRECIPITATION PRODUCT H05 (Version ' + sProgramVersion + ')]')
print('[' + sProjectName + '] Start Program ... ')
iExitStatus = 0
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# Algorithm Check
print('[' + sProjectName + '] Loading Library ... ')

# Check section
try:

    #-------------------------------------------------------------------------
    # Library import
    import traceback
    import os.path
    import datetime
    import time
    import sys
    
    from sys import argv
    from os.path import join
    
    # For debugging
    # import matplotlib.pyplot as plt
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # End section
    dStartTime = time.time()
    print('[' + sProjectName + '] Loading Library ... OK ')
    #----------------------------------------------------------------------------

except:

    #----------------------------------------------------------------------------
    # Algorithm exception(s)
    print('[' + sProjectName + '] ATTENTION - Loading Library ... FAILED')
    print('Program will be interrupted')
    oVarProgram = traceback.format_exc()
    print('Error: ' + oVarProgram)
    print('Info error:', sys.exc_info()[0])
    iExitStatus = -1
    sys.exit(iExitStatus)  # exit the program
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Parsering section
print('[' + sProjectName + '] Parsering settings file ... ')

# Check section
try:

    #----------------------------------------------------------------------------
    # Extracting script name from argument(s)
    try:
        sScriptName, sSettingsFile = argv
    except:
        sScriptName = argv
        sSettingsFile = None
        
    # Checking if settings file is defined or not
    if sSettingsFile != None:
        print(' ------> Settings file defined by user')
    else:
        print(' -------> ATTENTION: Default settings file')
        sSettingsFile = 'settings_precipitation_product_h05.txt'
    
    # Path main
    sPathMain = os.getcwd() + '/'  # Setting PathMain
    os.path.abspath(sPathMain)  # Entering in path main folder

    import GetSettings as GetSettings
    import GetGeoData_AsciiGrid as GetGeoData_AsciiGrid
    import GetSatData_AsciiGrid as GetSatData_AsciiGrid
    import GetTime as GetTime

    import ComputeProductData as ComputeProductData
    import SaveProductData as SaveProductData
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # Settings information
    oDataSettings = GetSettings.GetSettings(sSettingsFile)
    # Time information
    oDataTime = GetTime.GetTime(oDataSettings)
    # Geo data reference information
    oDataGeoRef = GetGeoData_AsciiGrid.GetGeoData_AsciiGrid(
                  join(oDataSettings.sPathDataStatic, oDataSettings.sFileNameRef))
    # Satellite data reference information
    oDataSatRef = GetSatData_AsciiGrid.GetSatData_AsciiGrid(
                  join(oDataSettings.sPathDataSatellite, oDataSettings.sFileNameSatellite))
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # End section
    print('[' + sProjectName + '] Parsering settings file ... OK')
    #----------------------------------------------------------------------------

except:

    #----------------------------------------------------------------------------
    # Algorithm exception(s)
    print('[' + sProjectName + '] ATTENTION - Parsering settings file ... FAILED')
    print('Program will be interrupted')
    oVarProgram = traceback.format_exc()
    print('Error: ' + oVarProgram)
    print('Info error:', sys.exc_info()[0])
    iExitStatus = -2
    sys.exit(iExitStatus)  # exit the program
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Real-time products
print('[' + sProjectName + '] Elaborating products ... ')

# Check section
try:
    
    #----------------------------------------------------------------------------
    # Cycling on date(s)
    for sTimeNow in oDataTime.a1sTimeRun:
    
        # Date information
        oTimeNow = datetime.datetime.strptime(sTimeNow,'%Y%m%d%H%M%S')
        sYearNow = oTimeNow.strftime('%Y'); sMonthNow = oTimeNow.strftime('%m')
        sDayNow = oTimeNow.strftime('%d')
        
        # Outcome data folder
        oDataSettings.sPathDataDynamicOutcomeStep = join(oDataSettings.sPathDataDynamicOutcome,sYearNow,sMonthNow,sDayNow,'')
        if not os.path.exists(oDataSettings.sPathDataDynamicOutcomeStep): os.makedirs(oDataSettings.sPathDataDynamicOutcomeStep)
        
        # Elaborating data
        oDriverCreate = ComputeProductData.ComputeProductData(sTimeNow, oDataTime, oDataGeoRef, oDataSatRef, oDataSettings)
        oDataProduct = oDriverCreate.CreateProduct()
        
        # Saving data
        oDriverSave = SaveProductData.SaveProductData(sTimeNow, oDataProduct, oDataTime, oDataGeoRef, oDataSettings)
        oDriverSave.SaveProduct()
         
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # End section         
    print('[' + sProjectName + '] Elaborating products ... OK')        
    #----------------------------------------------------------------------------

except:

    #----------------------------------------------------------------------------
    # Algorithm exception(s)
    print('[' + sProjectName + '] ATTENTION - Real-Time products ... FAILED')
    print('Program will be interrupted')
    oVarProgram = traceback.format_exc()
    print('Error: ' + oVarProgram)
    print('Info error:', sys.exc_info()[0])
    iExitStatus = -3
    sys.exit(iExitStatus)  # exit the program
    #----------------------------------------------------------------------------        

#-------------------------------------------------------------------------
# Note about script parameter(s)
print('NOTE - Algorithm parameter(s)')
print('Script: ' + str(sScriptName))
#-------------------------------------------------------------------------

#----------------------------------------------------------------------------
# End Program
dTimeElapsed = round(time.time() - dStartTime,1);

print('[' + sProjectName + '] - PRECIPITATION PRODUCT H05 (Version ' + sProgramVersion + ')]')
print('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
#----------------------------------------------------------------------------









































