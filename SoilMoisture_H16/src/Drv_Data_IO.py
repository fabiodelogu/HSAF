"""
Class Features:

Name:          Drv_Data_IO
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160609'
Version:       '2.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

from os.path import join
from os.path import split
from os.path import exists

from Lib_Op_System_Apps import defineFileExt
from Drv_Exception import Exc
#################################################################################

#################################################################################
# Check file binary
def checkBinaryFile(filename):
    """Return true if the given filename is binary.
    @raise EnvironmentError: if the file does not exist or cannot be accessed.
    @attention: found @ http://bytes.com/topic/python/answers/21222-determine-file-type-binary-text on 6/08/2010
    @author: Trent Mick <TrentM@ActiveState.com>
    @author: Jorge Orpinel <jorge@orpinel.com>"""

    if exists(filename):
        fin = open(filename, 'rb')
        try:
            CHUNKSIZE = 1024
            while 1:
                chunk = fin.read(CHUNKSIZE)
                if '\0' in chunk: # found null byte
                    return True
                if len(chunk) < CHUNKSIZE:
                    break # done
        finally:
            fin.close()

    return False
#################################################################################

#################################################################################
# Class to manage IO files
class Drv_Data_IO:
    
    #--------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFileName, sFileMode=None, sFileType=None):

        # Check binary file format
        bFileBinary = checkBinaryFile(sFileName)

        # Define file path, name and extension
        sFilePath = split(sFileName)[0]
        sFileName = split(sFileName)[1]
        sFileExt = defineFileExt(sFileName)

        # Define FileType and FileWorkspace
        if sFileName.endswith('txt') or sFileName.endswith('asc'):
            
            sFileType = 'ascii'
            self.oFileWorkspace = FileAscii(sFilePath, sFileName, sFileType, sFileMode)

        elif sFileName.endswith('nc'):
            
            sFileType = 'netCDF'
            self.oFileWorkspace = FileNetCDF(sFilePath, sFileName, sFileType, sFileMode)
            
        elif sFileName.endswith('tiff') or sFileName.endswith('tif'):
            
            sFileType = 'tiff'
            self.oFileWorkspace = FileTiff(sFilePath, sFileName, sFileType, sFileMode)
            
        elif sFileName.endswith('bin') or (sFileExt is '' and bFileBinary is True):
            
            sFileType = 'binary'
            self.oFileWorkspace = FileBinary(sFilePath, sFileName, sFileType, sFileMode)

        elif sFileName.endswith('mat'):
            
            sFileType = 'matlab'
            self.oFileWorkspace = FileMat(sFilePath, sFileName, sFileType, sFileMode)
        
        elif sFileName.endswith('grb') or sFileName.endswith('grib') or sFileType == 'grib':
            
            sFileType = 'grib'
            self.oFileWorkspace = FileGrib(sFilePath, sFileName, sFileType, sFileMode)
        
        elif sFileName.endswith('pickle'):
            
            sFileType = 'pickle'
            self.oFileWorkspace = FilePickle(sFilePath, sFileName, sFileType, sFileMode)
        
        elif sFileName.endswith('csv'):
            
            sFileType = 'csv'
            self.oFileWorkspace = FileCSV(sFilePath, sFileName, sFileType, sFileMode)
            
        elif sFileName.endswith('hdf') or sFileName.endswith('hdf4'):
            
            sFileType = 'hdf4'
            self.oFileWorkspace = FileHDF4(sFilePath, sFileName, sFileType, sFileMode)

        elif sFileName.endswith('hdf5') or sFileName.endswith('h5'):

            sFileType = 'hdf5'
            self.oFileWorkspace = FileHDF5(sFilePath, sFileName, sFileType, sFileMode)

        elif sFileName.endswith('buf') or sFileName.endswith('bufr') or sFileName.endswith('bfr'):
            
            sFileType = 'bufr'
            self.oFileWorkspace = FileBufr(sFilePath, sFileName, sFileType, sFileMode)
        
        else:
            sFileType = 'unknown'
            self.oFileWorkspace = FileUnknown(sFilePath, sFileName, sFileType, sFileMode)
    #--------------------------------------------------------------------------------
    
#################################################################################

#################################################################################

# --------------------------------------------------------------------------------
# Class to manage unknown files
class FileUnknown:

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Print file unknown information
        self.printInfo()

    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to print information about unknown file
    def printInfo(self):
        Exc.getExc(' -----> WARNING: file ' + join(self.sFilePath, self.sFileName) +
                   ' has unknown extension! Please check library or file format!', 2, 1)
        Exc.getExc(' -----> ERROR: file format unknown!', 1, 1)
    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Class to manage Bufr files
class FileBufr:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()
        
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):
        
        import Lib_Data_IO_Bufr as oFileLibrary
        self.oFileLibrary = oFileLibrary
        
    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Class to manage hdf5 files
class FileHDF5:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    oFileData = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):

        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()

    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):

        import Lib_Data_IO_HDF5 as oFileLibrary
        self.oFileLibrary = oFileLibrary

    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Class to manage hdf4 files
class FileHDF4:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()
        
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):

        import Lib_Data_IO_HDF4 as oFileLibrary
        self.oFileLibrary = oFileLibrary

    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Class to manage csv files
class FileCSV:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()
        
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):

        import Lib_Data_IO_CSV as oFileLibrary
        self.oFileLibrary = oFileLibrary

    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Class to manage pickle files
class FilePickle:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()
        
    # --------------------------------------------------------------------------------
    
    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):

        import Lib_Data_IO_Pickle as oFileLibrary
        self.oFileLibrary = oFileLibrary

    # --------------------------------------------------------------------------------
  
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Class to manage Grib files
class FileGrib:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()
        
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):

        import Lib_Data_IO_Grib as oFileLibrary
        self.oFileLibrary = oFileLibrary

    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Class to manage Mat files
class FileMat:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode
        
        # Set library IO
        self.setFileLibIO()
        
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):
        import Lib_Data_IO_Mat as oFileLibrary
        self.oFileLibrary = oFileLibrary

    # --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Class to manage Binary files
class FileBinary:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()
    
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):

        import Lib_Data_IO_Binary as oFileLibrary
        self.oFileLibrary = oFileLibrary

    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Class to manage Tiff files
class FileTiff:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()
        
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):
        
        import Lib_Data_IO_Tiff as oFileLibrary
        self.oFileLibrary = oFileLibrary
        
    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Class to manage ASCII files
class FileAscii:

    # --------------------------------------------------------------------------------
    # Class variable(s)
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()

    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):

        import Lib_Data_IO_Ascii as oFileLibrary
        self.oFileLibrary = oFileLibrary
        
    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Class to manage NetCDF grid files
class FileNetCDF:

    # --------------------------------------------------------------------------------
    # Class variables
    oFileLibrary = None
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Class init
    def __init__(self, sFilePath, sFileName, sFileType, sFileMode):
        
        # Common variable(s)
        self.sFilePath = sFilePath
        self.sFileName = sFileName
        self.sFileType = sFileType
        self.sFileMode = sFileMode

        # Set library IO
        self.setFileLibIO()

    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Method to set library I/O function(s)
    def setFileLibIO(self):
        
        import Lib_Data_IO_NetCDF as oFileLibrary
        self.oFileLibrary = oFileLibrary
        
    # --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

#################################################################################
