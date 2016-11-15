"""
Library Features:

Name:          Lib_Data_IO_NetCDF
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160615'
Version:       '2.0.0'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import numpy as np

# Global libraries
from Drv_Exception import Exc
#################################################################################

# ----------------------------------------------------------------------------
# Opening file
def openFile(sFileName, sFileMode, sFileFormat='NETCDF4'):

    try:
        from netCDF4 import Dataset
    except:
        from scipy.io.netcdf import netcdf_file as Dataset
        Exc.getExc(' -----> WARNING: NetCDF module import from scipy (usually imported from netcdf-python)!', 2, 1)

    try:
        # NetCDF type: NETCDF3_CLASSIC , NETCDF3_64BIT , NETCDF4_CLASSIC , NETCDF4
        oFile = Dataset(sFileName, sFileMode, format=sFileFormat)
        return oFile
    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_NetCDF)' + ' [' + str(oError) + ']', 1, 1)

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Closing file
def closeFile(oFile):
    oFile.close()
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Method to check variable name
def checkVarName(oFileData, sVarName):

    if sVarName in oFileData.variables:
        bVarExist = True
    else:
        bVarExist = False

    return bVarExist

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Get file attributes common
def getFileAttrsCommon(oFileData):

    oAttrs = oFileData.ncattrs()
    oAttrsFile = {}
    for sAttrName in oAttrs:

        oAttrValue = oFileData.getncattr(sAttrName.encode('utf-8'))

        if isinstance(oAttrValue, basestring):
            oAttrValue = oAttrValue.encode('utf-8')
        elif isinstance(oAttrValue, (np.float)):
            oAttrValue = np.float32(oAttrValue)
        elif isinstance(oAttrValue, (np.int32)):
            oAttrValue = np.int32(oAttrValue)
        elif isinstance(oAttrValue, (np.int64)):
            oAttrValue = np.int32(oAttrValue)
        else:
            Exc.getExc(' -----> ERROR: in reading file attribute(s). Attribute type not defined! (Lib_Data_IO_NetCDF)', 1, 1)

        oAttrsFile[sAttrName.encode('utf-8')] = oAttrValue

    return oAttrsFile

# ----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Get 2d variable (using variable name)
def get2DVar(oFileData, sVarName):

    try:
        a2dVarName_IN = oFileData.variables[sVarName][:]
        a2dVarName_OUT = np.transpose(np.rot90(a2dVarName_IN, -1))
    except:
        a2dVarName_OUT = None
        Exc.getExc(' -----> ERROR: in reading variable 2d. Check variable name! (Lib_Data_IO_NetCDF)', 1, 1)

    return a2dVarName_OUT
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Get 3d variable (using variable name)
def get3DVar(oFileData, sVarName):

    a3dVarName_IN = oFileData.variables[sVarName][:]

    a3dVarName_OUT = np.zeros([a3dVarName_IN.shape[1], a3dVarName_IN.shape[2], a3dVarName_IN.shape[0]])
    for iT in range(0,a3dVarName_IN.shape[0]):
        a2dVarName_IN = np.transpose(np.rot90(a3dVarName_IN[iT, :, :], -1))
        a3dVarName_OUT[:, :, iT] = a2dVarName_IN

        a2dVarName_IN[a2dVarName_IN < -900] = np.nan

        # Debug
        #plt.figure(1); plt.imshow(a2dVarName_IN); plt.colorbar(); plt.clim(-10,40);
        #plt.show()

    return a3dVarName_OUT
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to get all variable(s)
def getVars(oFileData):

    # Variable(s) initialization
    oDictData = {}

    # Get all variable names
    a1oFileVariables = oFileData.variables
    for sFileVariableKeys, sFileVariableName in a1oFileVariables.iteritems():
        # Convert variable name from Unicode to ASCII
        sFileVariable = sFileVariableKeys.encode('ascii', 'ignore')
        try:
            # Save variable in a dictionary
            oDataVariable = oFileData.variables[sFileVariableKeys][:]
            oDictData[sFileVariable] = oDataVariable
        except:
            pass

    return oDictData

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write field dimension
def writeDims(oFileData, sDimVar, iDimValue):

    # Dim declaration
    oFileData.createDimension(sDimVar, iDimValue)

    return oFileData

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write 3d variables
def write3DVar(oFileData, sVarName, a3dVarDataXYT, oVarAttr, sVarFormat, sVarDimT=None, sVarDimY=None, sVarDimX=None):

    # Creating variable
    oVar = oFileData.createVariable(sVarName, sVarFormat, (sVarDimT, sVarDimY, sVarDimX,), zlib = True)

    # Saving all variable attribute(s)
    for sVarAttr in oVarAttr:
        # Retrivieng attribute value
        sVarOptValue = oVarAttr[sVarAttr]
        # Saving attribute
        oVar.setncattr(sVarAttr.lower(),str(sVarOptValue))

    # Debug to check map orientation
    #if sVarName == 'Terrain':
    #    plt.figure(1)
    #    plt.imshow(np.transpose(np.rot90(a2dVarDataXY,-1))); plt.colorbar()
    #    plt.show()

    # Define 3d field(s)
    a3dVarDataTYX = np.zeros([a3dVarDataXYT.shape[2], a3dVarDataXYT.shape[0], a3dVarDataXYT.shape[1]])
    for iStep in range(0, a3dVarDataXYT.shape[2]):

        # Get data
        a2dVarDataXY = np.zeros([a3dVarDataXYT.shape[0], a3dVarDataXYT.shape[1]])
        a2dVarDataXY = a3dVarDataXYT[:,:, iStep]

        # Organize data
        a2dVarDataYX = np.zeros([a3dVarDataXYT.shape[0], a3dVarDataXYT.shape[1]])
        a2dVarDataYX = np.transpose(np.rot90(a2dVarDataXY,-1));

        # Store data
        a3dVarDataTYX[iStep, : , : ] = a2dVarDataYX

    # Save data
    oVar[:, :] = np.transpose(np.rot90(a3dVarDataXYT, -1))

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write 2d variables
def write2DVar(oFileData, sVarName, a2dVarDataXY, oVarAttr, sVarFormat, sVarDimY=None, sVarDimX=None):

    # Creating variable
    oVar = oFileData.createVariable(sVarName, sVarFormat, (sVarDimY, sVarDimX,), zlib = True)

    # Saving all variable attribute(s)
    for sVarAttr in oVarAttr:
        # Retrivieng attribute value
        sVarOptValue = oVarAttr[sVarAttr]
        # Saving attribute
        oVar.setncattr(sVarAttr.lower(),str(sVarOptValue))

    # Debug to check map orientation
    #if sVarName == 'Terrain':
    #    plt.figure(1)
    #    plt.imshow(np.transpose(np.rot90(a2dVarDataXY,-1))); plt.colorbar()
    #    plt.show()

    # Saving variable data
    oVar[:,:] = np.transpose(np.rot90(a2dVarDataXY, -1))

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write 1d variables
def write1DVar(oFileData, sVarName, a1dVarData, oVarAttr, sVarFormat, sVarDimY=None, sVarDimX=None):

    # Use Y var to create column array
    sVarDim = sVarDimY

    # Creating variable
    oVar = oFileData.createVariable(sVarName, sVarFormat, (sVarDim), zlib = True)
    # Saving all variable attribute(s)
    for sVarAttr in oVarAttr:
        # Retrivieng attribute value
        sVarOptValue = oVarAttr[sVarAttr]
        # Saving attribute
        oVar.setncattr(sVarAttr.lower(),str(sVarOptValue))

    # Saving variable data
    oVar[:] = a1dVarData

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to get time information
def getTime(oFileData):

    a1sTime = None;
    try:
        from datetime import datetime
        from netCDF4 import num2date, date2num

        oTime = oFileData.variables['time']
        a1oTime = num2date(oTime[:],units=oTime.units,calendar=oTime.calendar)

        a1sTime = []
        for oTime in a1oTime:
            sTime = oTime.strftime('%Y%m%d%H%M')
            a1sTime.append(sTime)
    except:
        a1sTime = None

    return sorted(a1sTime)
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to write time information
def writeTime(oFileData, oTime, sVarFormat='f8', sVarDimT=None, dTimeStep=None):

    from datetime import datetime
    from netCDF4 import num2date, date2num

    iTimeSteps = len(oTime)

    oDateFrom = datetime.strptime(oTime[0],'%Y%m%d%H%M')
    oDateTo = datetime.strptime(oTime[-1],'%Y%m%d%H%M')
    oDateRef = datetime.strptime('197001010000','%Y%m%d%H%M')

    dTimeStepCum = -dTimeStep
    a2iBnds = np.zeros([iTimeSteps,2])
    oDates = []; a1oBnds = []; a1dElapsed = []
    for iTime, sTime in enumerate(oTime):
        oDates.append(datetime(int(sTime[0:4]), int(sTime[4:6]), int(sTime[6:8]), int(sTime[8:10]), int(sTime[10:12])))

        a2iBnds[iTime][0] = dTimeStepCum
        a2iBnds[iTime][1] = dTimeStepCum + dTimeStep

        a1oBnds.append(dTimeStepCum)
        a1oBnds.append(dTimeStepCum + dTimeStep)

        a1dElapsed.append(dTimeStepCum)

        dTimeStepCum = dTimeStepCum + dTimeStep

    # Convert bnd from list to float
    a1dBnds = [float(iI) for iI in a1oBnds]

    # Times
    oTimes = oFileData.createVariable(sVarDimT, sVarFormat,(sVarDimT,))
    oTimes.calendar = 'gregorian'
    oTimes.units = 'hours since ' + oDateFrom.strftime('%Y-%m-%d %H:%M:%S')
    oTimes.bounds = 'time_bnds'

    oTimes[:] = date2num(oDates,units=oTimes.units, calendar=oTimes.calendar)

    # Time Bounds
    oTimeBounds = oFileData.createVariable('time_bnds','d',(sVarDimT, 'ntime',), zlib = True)
    oTimeBounds.time = str(np.array(a1dElapsed))
    oTimeBounds.time_bounds = a1dBnds
    oTimeBounds.time_date = str(np.array(oTime))
    oTimeBounds.datestart = oDateFrom.strftime('%Y-%m-%d %H:%M:%S')
    oTimeBounds.dateend = oDateTo.strftime('%Y-%m-%d %H:%M:%S')
    oTimeBounds.dateref = oDateRef.strftime('%Y-%m-%d %H:%M:%S')
    oTimeBounds.axis = 'T'

    oTimeBounds[:,:] = a2iBnds

    # Debug
    #oDates_Check = num2date(oTimes[:],units=oTimes.units,calendar=oTimes.calendar)
    #print(oDates_Check)

    return oFileData

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write common file attribute(s)
def writeFileAttrsCommon(oFileData, oFileAttributes, sFileName=None):

    import time

    # GENERAL ATTRIBUTE(S) ---> FROM FILE
    # Cycle on file attribute(s)
    for sFileAttr in oFileAttributes:
        # Retrieve attribute value
        sFileValue = oFileAttributes[sFileAttr]
        # Save attribute
        oFileData.setncattr(sFileAttr, sFileValue)

    # EXTRA ATTRIBUTE(S) ---> FROM SCRIPT
    if not sFileName is None:
        oFileData.filename = sFileName
    else:
        pass

    oFileData.filedate = 'Created ' + time.ctime(time.time())

    return oFileData

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write extra file attribute(s)
def writeFileAttrsExtra(oFileData, oParamsInfo, oGeoInfo):

    # Insert parameter(s) information
    for oParamKeys, oParamsValue in oParamsInfo.items():

        # Avoid save DB information in file(s)
        if oParamKeys != 'DB':

            if isinstance(oParamsValue,dict):
                sStrValues=''
                for sKey, dValue in oParamsValue.items():
                    sStrValues = sStrValues + sKey + ':' + str(dValue) + ';'
                oParamsValue = sStrValues
            else:
                pass

            oFileData.setncattr(oParamKeys.lower(), str(oParamsValue))

        else:
            pass

    # Insert geo information
    for oGeoKeys, oGeoValue in oGeoInfo.items():
        oFileData.setncattr(oGeoKeys.lower(), oGeoValue)

    return oFileData

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write array file attribute(s)
def writeFileAttrsArray(oFileData, sAttrName, oAttrArray):

    # Insert parameter(s) information
    a1oAttrValue = []
    for oAttrKeys, oAttrValue in oAttrArray.items():

        a1oAttrValue.append(str(oAttrKeys) + ':' + str(oAttrValue) + ' ')

    oFileData.setncattr(sAttrName.lower(), a1oAttrValue)

    return oFileData

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write geographical system
def writeGeoSystem(oFileData, oGeoSystemInfo, a1dGeoBox=None):

    # Open geosystem variable(s)
    oGeoSystem = oFileData.createVariable('crs','i')

    # Insert geobox
    if not a1dGeoBox is None:
        oGeoSystem.bounding_box = a1dGeoBox
    else:
        pass

    # Insert geosystem information
    for oGeoSystemKeys, oGeoSystemValue in oGeoSystemInfo.items():
        oGeoSystem.setncattr(oGeoSystemKeys.lower(), oGeoSystemValue)

    return oFileData

#----------------------------------------------------------------------------
