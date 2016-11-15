"""
Library Features:

Name:          Lib_Op_System_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20161018'
Version:       '2.0.3'
"""
#######################################################################################

# -------------------------------------------------------------------------------------
# Method to get regular expression from file
def getFileNameRegExp(a1oFileName, oFilePattern=r'\d{4}\d{2}\d{2}\d{2}\d{2}', oFileFilter=r'[^a-zA-Z0-9-]'):

    import re

    # Cycle(s) on filename(s)
    a1sRegExp = []
    for sFileName in a1oFileName:

        # Match date in filename(s)
        oMatch_Pattern = re.search(oFilePattern, sFileName)

        # Get date of filename(s)
        oMatch_Filter = re.compile(oFileFilter)
        sRegExp = oMatch_Pattern.group()
        sRegExp = oMatch_Filter.sub("", sRegExp)
        a1sRegExp.append(sRegExp)

    return a1sRegExp
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to create filename patterns
def createFileNamePattern(sFileName, oFileTags={}):
    for sFileKey, sFileTag in oFileTags.iteritems():
        sFileName_Upd = sFileName.replace(sFileKey, sFileTag)
    return sFileName_Upd

# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to select files in a given folder
def selectFileName(sPathName='', sFilePattern=None):
    from os.path import join, isfile

    if not sFilePattern:
        from os import listdir
        a1sFileName = [sFileName for sFileName in listdir(sPathName) if isfile(join(sPathName, sFileName))]
    else:
        import glob
        a1sFileName = glob.glob(join(sPathName, sFilePattern))
    return a1sFileName

# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to create folder (and check if folder exists)
def createFolder(sPathName='', sPathDeep=None):

    from os import makedirs
    from os.path import exists

    if sPathName != '':
        if sPathDeep:
            sPathNameSel = sPathName.split(sPathDeep)[0]
        else:
            sPathNameSel = sPathName

        if not exists(sPathNameSel):
            makedirs(sPathNameSel)
        else:
            pass
    else:
        pass
# -------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define dynamic folder name
def defineFolder(sFolderName='', oFileNameDict=None):

    if sFolderName != '':
        if not oFileNameDict:
            pass
        elif oFileNameDict:
            for sKey, sValue in oFileNameDict.items():
                sFolderName = sFolderName.replace(sKey, sValue)
        # Create folder on disk
        createFolder(sFolderName)
    else:
        pass

    return sFolderName

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define check file availability name
def checkFileName(sFileName):

    from os.path import isfile

    if isfile(sFileName):
        bFileAvailability = True
    else:
        bFileAvailability = False

    return bFileAvailability
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to define dynamic filename
def defineFileName(sFileName='', oFileNameDict=None):
    if sFileName != '':
        if not oFileNameDict:
            pass
        elif oFileNameDict:
            for sKey, sValue in oFileNameDict.items():
                sFileName = sFileName.replace(sKey, sValue)
    else:
        pass

    return sFileName

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#  Method to define file extension
def defineFileExt(sFileName=''):

    from os.path import splitext
    try:
        [sFileRoot, sFileExt] = splitext(sFileName)
    except:
        sFileRoot = splitext(sFileName)
        sFileExt = ''

    sFileExt = sFileExt.replace('.', '')

    return sFileExt
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to delete file
def deleteFileName(sFileName=''):

    from os import remove
    from os.path import exists

    if sFileName != '':
        # Delete file if exists
        if exists(sFileName):
            remove(sFileName)
        else:
            pass
    else:
        pass
# --------------------------------------------------------------------------------
