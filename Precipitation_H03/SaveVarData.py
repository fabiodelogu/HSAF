#----------------------------------------------------------------------------
'''
Class for saving data in hdf5 format
Created on Apr 07, 2014

@author: fabio
'''
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Libraries
import h5py
import time
import os.path

#import matplotlib.pylab as plt
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Class saveVarData
class SaveVarData:
    
    #----------------------------------------------------------------------------
    # Init class
    oFile = None
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Init class method
    def __init__(self, sFileName=None, oGeoDriver=None):
        
        self.sFileName = sFileName
        self.oGeoDriver = oGeoDriver
        
        self.oFile = None
        
        self.openFile()
        self.writeAttrFile()
        self.writeGeoRef()
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------   
    # Closing file 
    def closeFile(self):
        self.oFile.close()
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Opening file    
    def openFile(self):
        self.oFile = h5py.File(self.sFileName, 'w')
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Creating group
    def createGroup(self,sGroupName):
        
        oFile = self.oFile
        oGroup = oFile.create_group(sGroupName)
        
        return oGroup
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Writing georef file
    def writeGeoRef(self):
    
        if self.oGeoDriver:
            
            # Extracting georef and dims
            a2dGeoXRef = self.oGeoDriver.oGeoData.a2dGeoX
            a2dGeoYRef = self.oGeoDriver.oGeoData.a2dGeoY
            
            # Saving variable and features
            oFile = self.oFile
            
            # Saving variable on hdf5 (raw)
            
            sVarName = 'GeoX'; sVarStandardName = 'longitude'; sVarLongName = 'longitude'
            sVarCellMethod = ''; sVarCoordinates = ''; sVarUnits = 'degree'
            sVarGridMapping = ''; sVarModelDesc = 'Mask'; sVarModelName = ''
            a1dVarPalette = []; dVarNoData = []
            
            oDset = oFile.create_dataset(sVarName, data = a2dGeoXRef, compression='gzip', compression_opts=9)
            oDset.attrs["standard_name"] = sVarStandardName
            oDset.attrs["long_name"] = sVarLongName
            oDset.attrs["cell_method"] = sVarCellMethod
            oDset.attrs["coordinates"] = sVarCoordinates
            oDset.attrs["units"] = sVarUnits
            oDset.attrs["grid_mapping"] = sVarGridMapping
            oDset.attrs["model_description"] = sVarModelDesc
            oDset.attrs["model_name"] = sVarModelName
            #oDset.attrs["palette"] = a1dVarPalette
            #oDset.attrs["nodata"] = dVarNoData
            
            sVarName = 'GeoY'; sVarStandardName = 'latitude'; sVarLongName = 'latitude'
            sVarCellMethod = ''; sVarCoordinates = ''; sVarUnits = 'degree'
            sVarGridMapping = ''; sVarModelDesc = 'Mask'; sVarModelName = ''
            a1dVarPalette = []; dVarNoData = []
            
            oDset = oFile.create_dataset(sVarName, data = a2dGeoYRef, compression='gzip', compression_opts=9)
            oDset.attrs["standard_name"] = sVarStandardName
            oDset.attrs["long_name"] = sVarLongName
            oDset.attrs["cell_method"] = sVarCellMethod
            oDset.attrs["coordinates"] = sVarCoordinates
            oDset.attrs["units"] = sVarUnits
            oDset.attrs["grid_mapping"] = sVarGridMapping
            oDset.attrs["model_description"] = sVarModelDesc
            oDset.attrs["model_name"] = sVarModelName
            #oDset.attrs["palette"] = a1dVarPalette
            #oDset.attrs["nodata"] = dVarNoData
            
            self.oFile = oFile
            
        else:
            print('Georef undefined!')
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Writing 1d variables
    def writeVar1D(self, a1oVarData, sVarName):
        
        # Saving variable and features
        oFile = self.oFile
        oDset = oFile.create_dataset(sVarName, data = a1oVarData)
        self.oFile = oFile
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Writing global attribute
    def writeGlobalAttr(self, oVarValue, sVarName):
        
        # Saving global attribute
        oFile = self.oFile
        oFile.attrs[sVarName] = [str(oVarValue)]
        
        self.oFile = oFile
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Writing 2d variables 
    def writeVar2D(self, a2dVarDataXY, sVarName, a1dGeoBox,
                 sVarStandardName, sVarLongName, 
                 sVarCellMethod, sVarUnits,
                 sVarCoordinates, sVarGridMapping,
                 sVarModelDesc, sVarModelName,
                 sVarTimeInterp, sVarSpatialInterp, sVarSaveMethod,
                 a1dVarPalette, dVarNoData):
        
        # Saving variable and features
        oFile = self.oFile
        
        # Saving variable on hdf5 (raw)
        oDset = oFile.create_dataset(sVarName, data=a2dVarDataXY, compression='gzip', compression_opts=9)
        oDset.attrs["standard_name"] = sVarStandardName
        oDset.attrs["long_name"] = sVarLongName
        oDset.attrs["cell_method"] = sVarCellMethod
        oDset.attrs["coordinates"] = sVarCoordinates
        oDset.attrs["units"] = sVarUnits
        oDset.attrs["grid_mapping"] = sVarGridMapping
        oDset.attrs["model_description"] = sVarModelDesc
        oDset.attrs["model_name"] = sVarModelName
        oDset.attrs["time_interp"] = sVarTimeInterp
        oDset.attrs["spatial_interp"] = sVarSpatialInterp
        oDset.attrs["saving_method"] = sVarSaveMethod
        oDset.attrs["a1dGeoBox"] = a1dGeoBox
        oDset.attrs["palette"] = str(a1dVarPalette)
        oDset.attrs["nodata"] = dVarNoData

        self.oFile = oFile
    #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    # File Attributes
    def writeAttrFile(self):
        
        #----------------------------------------------------------------------------
        # Splitting filename and filepath
        sFilePath, sFileName = os.path.split(self.sFileName)
        #----------------------------------------------------------------------------

        #----------------------------------------------------------------------------
        # CF Conventions used to create file(s)
        self.oFile.attrs['Conventions'] = 'CF-1.5'
        # A succinct description of what is in the dataset
        self.oFile.attrs['title'] = ''
        # Specifies where the original data was produced
        self.oFile.attrs['institution'] ='CIMA Foundation - www.cimafoundation.org'
        # The method of production of the original data
        # Provide an audit trail for modifications to the original data
        self.oFile.attrs['history'] = ''
        # Published or web-based references that describes the data or methods used to produce it
        self.oFile.attrs['references'] = 'http://cf-pcmdi.llnl.gov/ ; http://cf-pcmdi.llnl.gov/documents/cf-standard-names/ecmwf-grib-mapping'
        # Miscellaneous information about the data or methods used to produce it
        self.oFile.attrs['comment'] = 'Author(s): Fabio Delogu, Simone Gabellani'
        # Email reference
        self.oFile.attrs['email'] = 'fabio.delogu@cimafoundation.org'
        
        # SECONDARY ATTRIBUTES
        self.oFile.attrs['projectinfo'] = 'HSAF Project'
        self.oFile.attrs['algorithm'] = 'Python Module for HSAF Products - Version 2.0.0 (20141204)'
        self.oFile.attrs['filename'] = sFileName
        self.oFile.attrs['filedate'] = 'Created ' + time.ctime(time.time())
        
        #----------------------------------------------------------------------------
        
        
        
        
        
        
        
        
        
        
        
        
