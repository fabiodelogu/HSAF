#-------------------------------------------------------------------------------------
# Class Features
__author__ = 'fabio'
__date__ = '20140425'
__version__ = '1.0.0'
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Libraries
import numpy as np
import glob
import datetime
import os
import re
import sys
from os.path import join

# Classes
import GetVarData as GetVarData
import ElabVarData as ElabVarData

# Debugging
#import matplotlib.pylab as plt
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Defining time file
def TimeFiles(sFileName, sTimeFormat):
    
    # Extract numbers from filename
    a1iTime = re.findall(r'\d+', sFileName)
    
    # Compose file time
    if (str(a1iTime[0]) == '03'):
        
        sTimeFile = sTimeFormat.replace('yyyymmdd', str(a1iTime[1]))
        sTimeFile = sTimeFile.replace('HHMMSS', str(a1iTime[2]))
        sProductFeat = 'one-layer'
        
    elif (str(a1iTime[0]) == '05'):
        
        sTimeFile = sTimeFormat.replace('yyyymmdd', str(a1iTime[1]))
        sTimeFile = sTimeFile.replace('HHMMSS', str(a1iTime[2]))   
        sProductFeat = str(a1iTime[3])
    
    elif (str(a1iTime[0]) == '10'):
        
        sTimeFile = sTimeFormat.replace('yyyymmdd', str(a1iTime[1]))
        sTimeFile = sTimeFile.replace('HHMMSS', '000000')   
        sProductFeat = 'one-layer'
    
    else:

        sys.exit(' ------> ATTENTION: product name is undefined! Check input file(s)!')
    
    if len(sTimeFile) < 14 :
        print(' ------> ATTENTION: unknown time format! Check it!')
    
    
    return sTimeFile, sProductFeat

#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Searching file(s)
def SearchFiles(sPathDataSource, sDataName, sFormatTime, sDataTime, sFileExt=None):
    
    
    #-------------------------------------------------------------------------------------  
    # Time definition
    oDataTime = datetime.datetime.strptime(sDataTime,'%Y%m%d%H%M%S')
    sDataYear = oDataTime.strftime('%Y'); sDataMonth = oDataTime.strftime('%m'); 
    sDataDay = oDataTime.strftime('%d'); sDataHour = oDataTime.strftime('%H')
    
    # Format time
    sFormatTime = sFormatTime.replace('yyyy', str(sDataYear))
    sFormatTime = sFormatTime.replace('mm', str(sDataMonth))
    sFormatTime = sFormatTime.replace('dd', str(sDataDay))  
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------  
    # Create str search (base on product name)
    if sDataName.lower() == 'h03':
        
        # Format time for product
        sFormatTime = sFormatTime.replace('HH', str(sDataHour))
        sFormatTime = sFormatTime.replace('MM', str('*'))                              
        
        # Example: h03_20141018_1542_rom.grb.gz
        sDateStrSearch =  sFormatTime + str(sFileExt)
    
    elif sDataName.lower() == 'h05':
        
        sFormatTime = sFormatTime.replace('HH', str(sDataHour))
        sFormatTime = sFormatTime.replace('MM', str('00')) 
        
        # Example: h05_20141018_0900_06_rom.grb.gz
        sDateStrSearch =  sFormatTime + '*' +  str(sFileExt)
        
    elif sDataName.lower() == 'h10':
        
        sFormatTime = sFormatTime
        
        # Example: h10_20141126_day_merged.H5
        sDateStrSearch =  sFormatTime + '*' +  str(sFileExt)
        
    else:
        sys.exit(' ------> ATTENTION: file(s) search failed! Check product(s) availability!')
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------  
    # Searching folder
    if glob.glob(sPathDataSource + '*' + sDataName.lower() +'*'):

        # File(s)
        a1sFileList = glob.glob(sPathDataSource + '*' + 
                                str(sDataName.lower()) + '*' + sDateStrSearch)
    #-------------------------------------------------------------------------------------  
        
    #-------------------------------------------------------------------------------------  
    # Check if data path exist
    if len(a1sFileList) == 0:
        
        if os.path.exists(str(sPathDataSource[0])):
        
            sPathDataStep = join(sPathDataSource, str(sDataYear), str(sDataMonth), str(sDataDay))
            a1sFileList = glob.glob(sPathDataStep + '*' + 
                              str(sDataName.lower()) + '*' + sDateStrSearch)
            a1sFileList.sort()
        else:
            print(' -------> ATTENTION: data path is not available! File(s) not found!')
            a1sFileList = []
            
    else:
        
        a1sFileList.sort()
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------  
    # Return variable(s)
    return a1sFileList
    #-------------------------------------------------------------------------------------  
    
#-------------------------------------------------------------------------------------    

#-------------------------------------------------------------------------------------    
# Compute product data class
class ComputeProductData:
    
    #-------------------------------------------------------------------------------------
    # Init variable(s)
    sTimeNow = None
    
    oSettings = None
    oTime = None
    oGeoRef = None
    oSatRef = None
    
    oData = None
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method time info
    def __init__(self, sTimeNow, oTime, oGeoRef, oSettings, oSatRef=None):
        
        # Saving global information
        self.sTimeNow = sTimeNow
        self.oTime = oTime
        self.oGeoRef = oGeoRef
        self.oSatRef = oSatRef
        self.oSettings = oSettings
        
        # Method for deleting file(s) that must be updated
        self.BufferProduct()
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Buffer product
    def BufferProduct(self):
        
        # Deleting buffer file (only for iTimeBuffer > 0)
        if self.oSettings.iTimeBuffer > 0:
        
            # Setting(s) information
            sFileNameOUT = self.oSettings.sFileNameOUT
            sProductNameOUT = self.oSettings.oDataSettings['Features']['ProductName']['NameOUT']
            sPathDataDynamicOutcome = self.oSettings.sPathDataDynamicOutcome
            
            # Defining timefrom and timeto
            oTimeTo = datetime.datetime.strptime(self.sTimeNow,'%Y%m%d%H%M')
            sTimeTo = oTimeTo.strftime('%Y%m%d%H%M')
            oTimeFrom = oTimeTo - datetime.timedelta(seconds = self.oSettings.iTimeBuffer)
            sTimeFrom = oTimeFrom.strftime('%Y%m%d%H%M')
            
            # Time buffer
            a1sTimeBuffer = np.unique([sTimeFrom[0:8], sTimeTo[0:8]])
            
            # Cycling on time(s) buffer
            for sTimeBuffer in a1sTimeBuffer:
                
                # Time buffer
                oTimeBuffer = datetime.datetime.strptime(sTimeBuffer,'%Y%m%d')
                
                # Date information
                sYearBuffer = oTimeBuffer.strftime('%Y'); sMonthBuffer = oTimeBuffer.strftime('%m')
                sDayBuffer = oTimeBuffer.strftime('%d')
                
                # Creating filename out
                sFileNameOUT = sFileNameOUT.replace('product',sProductNameOUT)
                sFileNameOUT = sFileNameOUT.replace('yyyy',sYearBuffer)
                sFileNameOUT = sFileNameOUT.replace('mm',sMonthBuffer)
                sFileNameOUT = sFileNameOUT.replace('dd',sDayBuffer)
                sFileNameOUT = sFileNameOUT.replace('HHMM','*')
                
                # Data folder
                sPathDataDynamicOutcomeStep = join(sPathDataDynamicOutcome,sYearBuffer,sMonthBuffer,sDayBuffer,'')
                
                # FileName(s) list
                a1sFileNameList = glob.glob(sPathDataDynamicOutcomeStep + sFileNameOUT);
                
                # Removing file(s) in buffer time
                for sFileNameList in a1sFileNameList:
                    os.remove(sFileNameList)
        
        else:
            pass
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Creating product
    def CreateProduct(self):
        
        # Elaborating step
        print(' --------------------- Time Reference ' + self.sTimeNow + ' --------------------- ')
        
        # Time now and product time
        sTimeNow = self.sTimeNow
        sProductTime = self.sTimeNow[0:8]
        
        # Product name(s)
        sProductNameIN = self.oSettings.oDataSettings['Features']['ProductName']['NameIN']
        sProductNameOUT = self.oSettings.oDataSettings['Features']['ProductName']['NameOUT']
        # Product time format
        sProductTimeFormatIN = self.oSettings.oDataSettings['Features']['ProductTime']['TimeFormatIN']
        sProductTimeFormatOUT = self.oSettings.oDataSettings['Features']['ProductTime']['TimeFormatOUT']
        
        # Product field(s)
        a1oProductFields = self.oSettings.oDataSettings['Fields']
        
        # Source data path
        sPathDataDynamicSource = self.oSettings.sPathDataDynamicSource
        sPathDataDynamicOutcomeStep = self.oSettings.sPathDataDynamicOutcomeStep
        
        # Extracting reference georef and dims
        a2dGeoXRef = self.oGeoRef.oGeoData.a2dGeoX
        a2dGeoYRef = self.oGeoRef.oGeoData.a2dGeoY
        #a1iGeoDataFinite = np.where(self.oGeoRef.a2bGeoDataFinite.ravel() == True)
        a1iGeoDataNan = np.where(self.oGeoRef.a2bGeoDataNan.ravel() == True )
        a1iGeoDims = a2dGeoXRef.shape
        
        # Extracting satellite georef
        #self.oSettings.a1dGeoXSat = self.oSatRef.a1dGeoSatX
        #self.oSettings.a1dGeoYSat = self.oSatRef.a1dGeoSatY
        
        # Searching file(s) in a folder     
        self.a1sProductFile = SearchFiles(sPathDataDynamicSource, 
                                          sProductNameIN, sProductTimeFormatIN, sTimeNow, 'gz')
        
        # Checking for available file(s)
        oData = {}; oDataElab = {}; a1sFileName = []
        if self.a1sProductFile:

            # Cycling on found file(s)
            for sProductFile in self.a1sProductFile:

                # Splitting path and filename
                sFilePath, sFileName = os.path.split(sProductFile)

                # Update product time (considering format yyyymmdd_HHMMSS)
                [sProductTime, sProductFeat] = TimeFiles(sFileName, sProductTimeFormatOUT)
                
                # Appending selected filename(s)
                if sProductFeat == 'one-layer':
                    a1sFileName = sFileName;
                else:
                    a1sFileName.append(sFileName)
                
                # Updating output filename 
                sFileNameOUT = self.oSettings.sFileNameOUT
                sFileNameOUT = sFileNameOUT.replace('product', sProductNameOUT)
                sFileNameOUT = sFileNameOUT.replace('yyyymmdd_HHMMSS', sProductTime)
                
                # File information
                print(' -------> Creating object file: ' + sFileNameOUT + ' (Field: '+sProductFeat+') ... ')
                
                # Checking file availability
                if not (os.path.isfile(join(sPathDataDynamicOutcomeStep,sFileNameOUT)) ):
                
                    # Getting and processing data
                    oDataRaw = GetVarData.GetVarData(sProductFile, a1oProductFields, self.oSettings)
                    oDataProc = ElabVarData.ElabVarData(self.oGeoRef, self.oSettings)
                    
                    # Checking dictionary initialization
                    if not sFileNameOUT in oData.keys():
                        oData[sFileNameOUT] = {}

                    # Checking data product    
                    if oDataRaw.oDataProduct != None:
                        
                        oDataWorkspace = oDataRaw.oDataProduct
                        oDataProc.gridVar(oDataWorkspace)
                        
                        a1oDataElab = oDataProc.oDataProduct['Data']
                        
                        # Checking if data exists
                        if a1oDataElab is not None and np.any(np.isfinite(a1oDataElab.values())):
                            
                            # Cycling on variable(s)
                            oDataElab = {}; 
                            for sVarData in a1oDataElab:
                                
                                # Variable info
                                print(' ------> Elaborating ' + sVarData + ' dynamic variable ...')
                                
                                # Variable limits and nodata
                                oVarMin = self.oSettings.oDataSettings['Fields'][sVarData]['Lim_Min']
                                oVarMax = self.oSettings.oDataSettings['Fields'][sVarData]['Lim_Max']      
                                dVarNoData = self.oSettings.oDataSettings['Fields'][sVarData]['Attrs']['nodata']
                                
                                # Using 1d and 2d arrays
                                a1dDataElab = a1oDataElab[sVarData].ravel() 
                                
                                # Checking min limit
                                if not oVarMin is None:
                                    dVarMin = float(oVarMin)
                                    a1dDataElab[a1dDataElab<dVarMin] = np.nan
                                # Checking max limit
                                if not oVarMax is None:
                                    dVarMax = float(oVarMax)
                                    a1dDataElab[a1dDataElab>dVarMax] = np.nan
                                
                                a1dDataElab[a1iGeoDataNan] = dVarNoData
                                a2dDataElab = np.reshape(a1dDataElab,(a1iGeoDims[0],a1iGeoDims[1]))

                                # Debug
                                #plt.figure(1);plt.imshow(a2dDataElab);plt.colorbar();plt.show()
                                
                                # Saving in a dict
                                oDataElab[sVarData] = a2dDataElab
                                print(' ------> Elaborating ' + sVarData + ' dynamic variable ... OK')
                                
                        else:
                            # No data on domain
                            oDataElab = {}
                            pass
                        
                        # File information
                        print(' -------> Creating object file: ' + sFileNameOUT + ' (Field: '+sProductFeat+') ... OK')
                        
                    else:
                        # No data into file
                        oDataElab = {}
                        pass
                
                else:
                    
                    # Exit if file was created previously
                    print(' -------> Creating object file: ' + sFileNameOUT + ' (Field: '+sProductFeat+') ... File created previously')
                    oDataElab = None
                
                # Saving all fields 
                print(' -------> Storing object file: ' + sFileNameOUT + ' (Field: '+sProductFeat+') ... ')
                if (oDataElab):
                    
                    # Checking if data is initialized
                    #if not any(oData.values()):
                    oData[sFileNameOUT]['GeoX'] = a2dGeoXRef
                    oData[sFileNameOUT]['GeoY'] = a2dGeoYRef
                    oData[sFileNameOUT]['FileNameOutcome'] = sFileNameOUT
                    oData[sFileNameOUT]['FileDate'] = sTimeNow
                    oData[sFileNameOUT]['DateStep'] = sProductTime
                    oData[sFileNameOUT]['ProductNameInput'] = sProductNameIN
                    oData[sFileNameOUT]['ProductNameOutcome'] = sProductNameOUT
                    oData[sFileNameOUT]['FileNameInput'] = a1sFileName
                    
                    oData[sFileNameOUT][sProductFeat] = {}
                    oData[sFileNameOUT][sProductFeat]['Data'] = oDataElab
                    
                    # Saving data in dictionary according to product features
                    #if sProductFeat == '':
                    #    oData[sFileNameOUT]['Data'] = oDataElab
                    #else:
                    #    oData[sFileNameOUT][sProductFeat] = {}
                    #    oData[sFileNameOUT][sProductFeat]['Data'] = oDataElab
                    
                    print(' -------> Storing object file: ' + sFileNameOUT + ' (Field: '+sProductFeat+') ... OK')
                
                elif(oDataElab is None):
                    
                    # Exit if file was created previously
                    oData[sFileNameOUT] = None

                    # Exit Info
                    print(' -------> Storing object file: ' + sFileNameOUT + ' (Field: '+sProductFeat+') ... File created previously')
                
                else: 
                    
                    # Other cases
                    print(' -------> ATTENTION: no data available! Check input data!')

        else:
            # Initializing data product with none value
            print(' -------> ATTENTION: product file(s) are not available!')
        
        # Exit with data dictionary
        return oData
                
    #-------------------------------------------------------------------------------------
        


        

        
        
        
