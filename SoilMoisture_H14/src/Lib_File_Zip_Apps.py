"""
Library Features:

Name:          Lib_File_Zip_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160616'
Version:       '2.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
import os

from os.path import isfile

from Drv_Exception import Exc
#################################################################################

# --------------------------------------------------------------------------------
# Zip format dictionary
oZipDict = dict(Type_1='gz', Type_2='bz2', Type_3='7z', Type_4='tar',
                Type_5='tar.gz', Type_6='tar.7z', Type_7='zip')
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to delete FileName unzip
def removeFileUnzip(sFileName_UNZIP, bFileName_DEL=False):
    if bFileName_DEL is True:
        if isfile(sFileName_UNZIP):
            os.remove(sFileName_UNZIP)
        else:
            pass
    else:
        pass
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to delete FileName zip
def removeFileZip(sFileName_ZIP, bFileName_DEL=False):
    if bFileName_DEL is True:
        if isfile(sFileName_ZIP):
            os.remove(sFileName_ZIP)
        else:
            pass
    else:
        pass
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to get zip extension using filename
def getFileExtZip(sFileName):

    for sZipDict in oZipDict.values():
        iCharLen = len(sZipDict)
        iFileLen = len(sFileName)

        if sFileName.endswith(sZipDict, (iFileLen - iCharLen), iFileLen):
            sZipType = sZipDict
            bZipType = True
            break
        else:
            sZipType = None
            bZipType = True

    return sZipType, bZipType
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to check if a file has zip extension
def checkFileNameZip(sFileName_IN, sZipExt='NoZip'):

    # Check if string starts with point
    if sZipExt.startswith('.'):
        sZipExt = sZipExt[1:]
    else:
        pass

    # Check if zip extension is activated
    if not (sZipExt == 'NoZip' or sZipExt == ''):
        # Check zip extension format
        [sZipExt, bZipExt] = checkFileExtZip(sZipExt)

        if bZipExt:
            if sZipExt in sFileName_IN:
                sFileName_OUT = sFileName_IN
            else:
                sFileName_OUT = sFileName_IN + '.' + sZipExt
        else:
            Exc.getExc(" -----> WARNING: sZipExt selected is not known extension! Add in zip dictionary if necessary!", 2, 1)
            sFileName_OUT = sFileName_IN
    else:
        sFileName_OUT = sFileName_IN
    return sFileName_OUT

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to check if zip extension is a known string
def checkFileExtZip(sZipExt):

    # Check if string starts with point
    if sZipExt.startswith('.'):
        sZipExt = sZipExt[1:]
    else:
        pass

    # Check if zip extension is a known string
    if sZipExt in oZipDict.values():
        bZipExt = True
    else:
        bZipExt = False

    return sZipExt, bZipExt

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to add zip extension to filename
def addFileExtZip(sFileName_UNZIP, sZipExt=''):

    if sZipExt is not '':

        # Check zip extension format
        [sZipExt, bZipExt] = checkFileExtZip(sZipExt)

        # Create zip filename
        sFileName_ZIP = ''
        if bZipExt is True:
            sFileName_ZIP = ''.join([sFileName_UNZIP, '.', sZipExt])
        elif bZipExt is False:
            Exc.getExc(" -----> WARNING: sZipExt selected is not known extension! Add in zip dictionary if necessary!", 2, 1)
            sFileName_ZIP = ''.join([sFileName_UNZIP, '.', sZipExt])
        else:
            Exc.getExc(" -----> ERROR: error in selection sZipExt extension! Check in zip dictionary!", 1, 1)

    else:
        sFileName_ZIP = sFileName_UNZIP

    return sFileName_ZIP, sZipExt

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to remove only compressed extension 
def removeFileExtZip(sFileName_ZIP, sZipExt=''):

    # Check zip extension format
    if sZipExt is not '':
        # Check zip extension format in selected mode
        [sZipExt, bZipExt] = checkFileExtZip(sZipExt)
    else:
        # Check zip extension format in default mode
        Exc.getExc(" -----> WARNING: sZipExt is undefined! Searching zip extension in default mode!", 2,1)
        sFileName_UNZIP, sZipExt = os.path.splitext(sFileName_ZIP)
        # Check zip extension format
        [sZipExt, bZipExt] = checkFileExtZip(sZipExt)

    # Create zip filename
    sFileName_UNZIP = ''
    if bZipExt is True:
        sFileName_UNZIP = sFileName_ZIP.split(sZipExt)[0]
        if sFileName_UNZIP.endswith('.'):
            sFileName_UNZIP = sFileName_UNZIP[0:-1]
        else:
            pass

    elif bZipExt is False:
        Exc.getExc(" -----> WARNING: sZipExt selected is not known extension! Add in zip dictionary if necessary!", 2, 1)
        [sFileName_UNZIP, sZipExt] = os.path.splitext(sFileName_ZIP)
    else:
        Exc.getExc(" -----> ERROR: error in selection sZipExt extension! Check in zip dictionary!", 1, 1)

    return sFileName_UNZIP, sZipExt
# --------------------------------------------------------------------------------










