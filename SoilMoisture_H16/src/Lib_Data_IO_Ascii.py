"""
Library Features:

Name:          Lib_Data_IO_Ascii
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160609'
Version:       '2.0.0'
"""
#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
from Drv_Exception import Exc
#################################################################################

# --------------------------------------------------------------------------------
# Method to open ASCII file (in read or write mode)
def openFile(sFileName, sFileMode):
    try:
        oFile = open(sFileName, sFileMode)
        return oFile
    except IOError as oError:
        Exc.getExc(' -----> ERROR: in open file (Lib_Data_IO_Ascii)' + ' [' + str(oError) + ']', 1, 1)
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to close ASCII file
def closeFile(oFile):
    oFile.close()
# --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Read ArcGrid data
def readArcGrid(oFile):

    # Check method
    try:

        import numpy as np
        from string import atof, atoi, split

        # Read Header
        a1oVarHeader = {
            "ncols"        : atoi(split(oFile.readline())[1]),
            "nrows"        : atoi(split(oFile.readline())[1]),
            "xllcorner"    : atof(split(oFile.readline())[1]),
            "yllcorner"    : atof(split(oFile.readline())[1]),
            "cellsize"     : atof(split(oFile.readline())[1]),
            "NODATA_value" : atof(split(oFile.readline())[1]),
        }

        iNCols = a1oVarHeader["ncols"]; iNRows = a1oVarHeader["nrows"]

        # Read grid values
        a2dVarData = np.zeros((iNRows, iNCols))
        a2dVarData = np.loadtxt(oFile, skiprows=0)

        # Debugging
        #plt.figure(1)
        #plt.imshow(a2dVarData); plt.colorbar();
        #plt.show()

        return a2dVarData, a1oVarHeader

    except:
        # Exit status with error
        Exc.getExc(' -----> ERROR: in readArcGrid function (Lib_Data_IO_Ascii)',1,1)

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Write 2dVar
def writeArcGrid(oFile, a2dVarData, a1oVarHeader, sDataFormat=None):

    import numpy as np

    # sDataFormat: f, i, None

    # Check method
    try:

        # Defining max number of digits before comma
            dVarDataMin = np.nanmin(np.unique(a2dVarData))
            dVarDataMax = np.nanmax(np.unique(a2dVarData))
            iVarDataMax = int(dVarDataMax)

            # Get data format and digits
            if sDataFormat == 'f':
                iDigitNum = len(str(iVarDataMax)) + 3
                sFmt = '%'+str(iDigitNum)+'.2' + sDataFormat
            elif sDataFormat == 'i':
                iDigitNum = len(str(iVarDataMax))
                sFmt = '%'+str(iDigitNum) + sDataFormat
            else:
                Exc.getExc(' -----> WARNING: data format unknown! Set float type!', 2, 1)
                iDigitNum = len(str(iVarDataMax)) + 3
                sFmt = '%'+str(iDigitNum)+'.2' + sDataFormat

            # Write header
            oFile.write("ncols\t%i\n" % a1oVarHeader["ncols"])
            oFile.write("nrows\t%i\n" % a1oVarHeader["nrows"])
            oFile.write("xllcorner\t%f\n" % a1oVarHeader["xllcorner"])
            oFile.write("yllcorner\t%f\n" % a1oVarHeader["yllcorner"])
            oFile.write("cellsize\t%f\n" % a1oVarHeader["cellsize"])
            if sDataFormat == 'f':
                oFile.write("NODATA_value\t%f\n" % a1oVarHeader["NODATA_value"])
            elif sDataFormat == 'i':
                oFile.write("NODATA_value\t%i\n" % a1oVarHeader["NODATA_value"])
            else:
                Exc.getExc(' -----> WARNING: no data format set in float type!', 2, 1)
                oFile.write("NODATA_value\t%f\n" % a1oVarHeader["NODATA_value"])

            # Write grid values
            #sDataFormat = '%'+str(iDigitNum)+'.2f';
            np.savetxt(oFile, a2dVarData, delimiter=' ', fmt=sFmt,  newline='\n')

    except:
        # Exit status with error
        Exc.getExc(' -----> ERROR: in writeArcGrid function (Lib_Data_IO_Ascii)', 1, 1)

    #----------------------------------------------------------------------------
    
#----------------------------------------------------------------------------
