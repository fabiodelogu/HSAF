#-------------------------------------------------------------------------------------
# Class Features
__author__ = 'fabio'
__date__ = '20140415'
__version__ = '1.5.0'
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Library
import pygrib
import h5py
#import bufr
import os
import numpy as np
import bz2
import gzip
import sys
import re
from os.path import join

# Debugging
#import matplotlib.pylab as plt
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Class reading settings
class GetVarData:

    #-------------------------------------------------------------------------------------
    # Init vars
    sFileName = None
    a1oFieldsName = None
    oSettings = None
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, sFileName=None, a1oFieldsName=None, oSettings=None):
        
        # FileName
        self.sFileName = sFileName
        self.oSettings = oSettings
        self.a1oFieldsName = a1oFieldsName
        
        # Checking if file is compressed
        self.unzipfile()
        
        # Opening file grib
        if self.sFileName.endswith('grb') or self.sFileName.endswith('grib'):  # file grib
            
            #print('File GRIB')
            self.openfilegrib()
            
        elif self.sFileName.endswith('hdf5') or self.sFileName.endswith('H5') : # file hdf5
            
            #print('File HDF5')
            self.openfilehdf5()
            
        elif self.sFileName.endswith('buf'): # file bufr
            
            #print('File BUFR')
            self.openfilebufr()
            
        else:
            sys.exit(' -------> ATTENTION: unknown file format!') 

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Unzipping file(s) in bz2, gzip format(s)
    def unzipfile(self):
        
        # Filename
        sFileNameZip = self.sFileName
        
        # Defining filename
        sFilePath, sFileNameZip = os.path.split(sFileNameZip)
        a1sFilePart = sFileNameZip.split('.')
        
        # Defining unzipped filename
        if len(a1sFilePart) == 3:
            sFileNameUnzip = a1sFilePart[0] + '.' + a1sFilePart[1]
            
        # Choosing compressed format
        if(sFileNameZip.endswith('bz2')):
            
            # Uncompressed file 
            oCompressData = bz2.BZ2File(join(sFilePath, sFileNameZip))
            oDecompressData = oCompressData.read()
            oFileUnzip = open(join(sFilePath, sFileNameUnzip), "wb")
            oFileUnzip.write(oDecompressData)
            
            # Updating filename 
            self.sFileName = join(sFilePath,sFileNameUnzip)
            
        elif(sFileNameZip.endswith('gz')):

			print(' -----> gzip ')
			# Uncompressed file 
			oCompressData = gzip.GzipFile(join(sFilePath,sFileNameZip), "rb")
			oDecompressData = oCompressData.read()
			oFileUnzip = open(join(sFilePath, sFileNameUnzip), "wb")
			oFileUnzip.write(oDecompressData)

			# Updating filename 
			self.sFileName = join(sFilePath,sFileNameUnzip)
			print(' -----> fine gzip ')

        else:
            # Uncompressed file
            print(' ------> File Unzipped')
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Opening file bufr
    def openfilebufr(self):
        import bufr
        # Loading settings
        oSettings = self.oSettings.oDataInputOptions      
        sProductName = self.sProductName
         
        oDataInput = oSettings['VariablesInput_' + sProductName]

        # Creating variables dictionary
        oVarDict = {}
        for sVarName in oDataInput:
            oVarDict[sVarName] = oDataInput[sVarName]['long_name']
            
        # Opening file
        oFile = bufr.BUFRFile(self.sFileName);
        sFileName = oFile.filename
        
        # Defining filename
        sFilePath, sFileName = os.path.split(sFileName)
        # Definining datefile
        a1sFilePart = sFileName.split('.')
        a1sFilePart = a1sFilePart[0].split('_')
        if len(a1sFilePart) == 6:
            sDate = str(a1sFilePart[1]) + str(a1sFilePart[2])
            sProductNameRaw = str(a1sFilePart[0])
        else:
            print('ATTENTION: CHECK BUFR FILENAME!!!')
            sDate = str(a1sFilePart[2]) + str(a1sFilePart[3])
            sProductNameRaw = str(a1sFilePart[1])
        
        # Checking data quality
        try:

            a1oListVar = oVarDict.values()
            a1oListKeys = oVarDict.keys()
            oValue = {}; 
            for a1oField in oFile:
    
                # Un-packing all records in file 
                for a1oRecord in a1oField:
                    
                    # Selection of bufr variable
                    sVarName = a1oRecord.name
    
                    # Extracting selected variables
                    if sVarName.rstrip() in a1oListVar:
                        
                        iVarIndex = []
                        iVarIndex = a1oListVar.index(sVarName.rstrip())
    
                        sVarKey = a1oListKeys[iVarIndex]
                    
                        a1dValuePatch = [];
                        a1dValuePatch = a1oRecord.data
  
                        try:
                            a1dValue = oValue[sVarName.rstrip()]
                        except:
                            a1dValue = []
                            
                        oValue[sVarKey.rstrip()] = np.append(a1dValue,a1dValuePatch)
            
            # GeoX and GeoY             
            a1dGeoX = oValue['HSAF_Product_H07_GeoX']
            del oValue['HSAF_Product_H07_GeoX']
            a1dGeoY =  oValue['HSAF_Product_H07_GeoY']
            del oValue['HSAF_Product_H07_GeoY']
            
        except:
            oValue = None
            a1dGeoX = None
            a1dGeoY = None
            sFileName = sFileName
            sProductName = None
        
        # Saving all fields 
        oData = {}
        oData['GeoX'] = a1dGeoX
        oData['GeoY'] = a1dGeoY
        oData['FileNameInput'] = sFileName
        oData['FileNameOutcome'] = None
        oData['Data'] = oValue
        oData['FileDate'] = sDate
        oData['DateStep'] = sDate
        oData['ProductNameInput'] = sProductNameRaw.upper()
        oData['ProductNameOutcome'] = None
        
        self.oDataProduct = oData
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Opening file grib
    def openfilegrib(self):
        
        # Flag to delete temporary file(s)
        iTempFileDelete = self.oSettings.iTempFileDelete
        
        # Opening file
        oFile = pygrib.open(self.sFileName)
        sFileName = oFile.name
        
        # Defining filename(s)
        a1oFieldsName = self.a1oFieldsName
        
        # Defining filename
        sFilePath, sFileName = os.path.split(sFileName)
        
        a1sFilePart = sFileName.split('.')
        a1sFilePart = a1sFilePart[0].split('_')
        
        # File information (open)
        print(' -------> Getting file: ' + sFileName + ' ... ')
        
        # Parsering date and product name
        if (len(a1sFilePart) == 6):
            
            sProductName = str(a1sFilePart[2]) + '_' + str(a1sFilePart[3])
            sProductTime = str(a1sFilePart[5])
            
        elif (len(a1sFilePart) == 5):
            
            sProductName = str(a1sFilePart[0])
            sProductName = 'h' + str(re.findall(r'\d+', sProductName)[0])
            
            if sProductName == 'h05':
                sProductTime = str(a1sFilePart[0]) + str(a1sFilePart[1]) 
                sProductType = str(a1sFilePart[3])
            
        elif (len(a1sFilePart) == 4):
            
            sProductName = str(a1sFilePart[0])
            sProductName = 'h' + str(re.findall(r'\d+', sProductName)[0])
            
            if sProductName == 'h03':
                sProductTime = str(a1sFilePart[1]) + str(a1sFilePart[2]) 
                sProductType = ''
            
        else:
            
            sys.exit(' ------> ATTENTION: unknown filename or time format!') 
        

        # Cycling on selected field(s)
        oDict = {}; 
        for sFieldName in a1oFieldsName.keys():
        
            # Defining field name(s)
            sFieldNameIN = a1oFieldsName[sFieldName]['NameIN']
            sFieldNameOUT = a1oFieldsName[sFieldName]['NameOUT']
            dScaleFactor = float(a1oFieldsName[sFieldName]['ScaleFactor']);
            dNoData = float(a1oFieldsName[sFieldName]['NoData']);
            
            # Check product version and variable(s)
            if( sProductName == 'h03' or sProductName == 'h05'):
                if not (sFieldName == 'Latitude' or sFieldName == 'Longitude'):
                    
                    # Field info
                    sFieldNameOUT =  sFieldNameOUT.replace('HH', sProductType)
                    print(' ------> Saving ' + sFieldName + ' in dynamic variable(s) ... ')
                    
                    # Grib message
                    oFileData = oFile[1]
                    
                    # Data 
                    a2dDataMasked = oFileData.values
                    a2dData = a2dDataMasked.data
                    
                    # No data values and flipping data
                    a2dData[a2dData==dNoData] = np.nan
                    #a2dData = np.flipud(a2dData)
                    a1iDataDims = a2dData.shape
                    
                    # Scale factor
                    a2dData = a2dData*dScaleFactor
                    
                    # Geocoord
                    #[a2dGeoY, a2dGeoX] = oFileData.latlons()
                    a2dGeoX = np.reshape(self.oSettings.a1dGeoXSat,[a1iDataDims[0], a1iDataDims[1]])
                    a2dGeoY = np.reshape(self.oSettings.a1dGeoYSat,[a1iDataDims[0], a1iDataDims[1]])
 
                    # Saving data in a dictionary
                    oDict[str(sFieldName)] = a2dData
                    
                    # Field exit
                    print(' ------> Saving ' + sFieldName + ' in dynamic variable(s) ... OK')
            
                elif (sFieldName == 'Latitude' or sFieldName == 'Longitude'):
                
                    print(' ------> ATTENTION: ' + sFieldName + ' skipped in saving dynamic variable(s)!')
            
            else:
                
                sys.exit(' ------> ATTENTION: unkwnon data!')
        
        # Deleting temporary file(s)
        if iTempFileDelete == 1:
            os.remove(join(sFilePath, sFileName))
        else:
            pass
            
        
        # Debugging
        #plt.figure(1)
        #plt.imshow(a2dGeoX); plt.colorbar();
        #plt.figure(2)
        #plt.imshow(a2dGeoY); plt.colorbar();
        #plt.figure(3)
        #plt.imshow(a2dData); plt.colorbar();
        #plt.show()
        
        # Saving all fields 
        oData = {}
        oData['GeoX'] = a2dGeoX
        oData['GeoY'] = a2dGeoY
        oData['FileNameInput'] = sFileName
        oData['FileNameOutcome'] = None
        oData['Data'] = oDict
        oData['FileDate'] = sProductTime
        oData['DateStep'] = sProductTime
        oData['ProductNameInput'] = sProductName
        oData['ProductNameOutcome'] = None
        
        # File information (close)
        print(' -------> Getting file: ' + sFileName + ' ... OK')
        
        self.oDataProduct = oData
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Opening file hdf5
    def openfilehdf5(self):
        
        # Flag to delete temporary file(s)
        iTempFileDelete = self.oSettings.iTempFileDelete
        
        # Opening file
        oFile = h5py.File(self.sFileName,'r')
        sFileName = oFile.filename
        
        # Defining filename(s)
        a1oFieldsName = self.a1oFieldsName
        
        # Defining filename
        sFilePath, sFileName = os.path.split(sFileName)
        
        a1sFilePart = sFileName.split('.')
        a1sFilePart = a1sFilePart[0].split('_')
        
        # File information (open)
        print(' -------> Getting file: ' + sFileName + ' ... ')
        
        # Parsering date and product name
        if (len(a1sFilePart) == 6):
            
            sProductName = str(a1sFilePart[2]) + '_' + str(a1sFilePart[3])
            sProductTime = str(a1sFilePart[5])
            
        elif (len(a1sFilePart) == 5):
            
            sProductName = str(a1sFilePart[2]) + '_' + str(a1sFilePart[3])
            sProductTime = str(a1sFilePart[4])    
            
        elif (len(a1sFilePart) == 4):
            
            sProductName = str(a1sFilePart[0])
            sProductTime = str(a1sFilePart[1])    
            
        else:
            
            sys.exit(' -------> ATTENTION: unknown filename or time format!') 
        
        # Cycling on selected field(s)
        oDict = {}; 
        for sFieldName in a1oFieldsName.keys():
            
            # Field info
            print(' ------> Saving ' + sFieldName + ' in dynamic variable(s) ... ')
            
            # Defining field name(s)
            sFieldNameIN = a1oFieldsName[sFieldName]['NameIN']
            sFieldNameOUT = a1oFieldsName[sFieldName]['NameOUT']
            dScaleFactor = float(a1oFieldsName[sFieldName]['ScaleFactor']);
            dNoData = float(a1oFieldsName[sFieldName]['NoData']);
            oMask = a1oFieldsName[sFieldName]['Mask'];
            
            # Extracting data 
            oDatasetName = oFile[str(sFieldNameIN)]
            
            # Data conversion and nodata value definition
            oData = oDatasetName.value
            a2dData = oData.astype(float)
            
            # Defining map values (if mask is defined)
            if(len(oMask)>0):
                
                for sFieldMask in oMask.keys():
                    
                    dValueRaw = float(oMask[sFieldMask]['iValueRaw'])
                    dValueMap = float(oMask[sFieldMask]['iValueMap'])
                    
                    a2dData[a2dData == dValueRaw] = dValueMap
            
            a2dData[a2dData == dNoData] = np.nan
            a2dData = a2dData/dScaleFactor
            
            # Saving data in a dictionary
            oDict[str(sFieldName)] = a2dData
            
            # Field exit
            print(' ------> Saving ' + sFieldName + ' in dynamic variable(s) ... OK')
        
        # Deleting temporary file(s)
        if iTempFileDelete == 1:
            os.remove(join(sFilePath, sFileName))
        else:
            pass
        
        # GeoX and GeoY and filename(s)          
        a2dGeoX = oDict['Longitude']
        del oDict['Longitude']
        a2dGeoY =  oDict['Latitude']
        del oDict['Latitude']
        
        # Saving all fields 
        oData = {}
        oData['GeoX'] = a2dGeoX
        oData['GeoY'] = a2dGeoY
        oData['FileNameInput'] = sFileName
        oData['FileNameOutcome'] = None
        oData['Data'] = oDict
        oData['FileDate'] = sProductTime
        oData['DateStep'] = sProductTime
        oData['ProductNameInput'] = sProductName
        oData['ProductNameOutcome'] = None
        
        # File information (close)
        print(' -------> Getting file: ' + sFileName + ' ... OK')
        
        self.oDataProduct = oData
    #-------------------------------------------------------------------------------------

