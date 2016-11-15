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
import os
from os.path import join

# Classes
import SaveVarData as SaveVarData

# Debugging
#import matplotlib.pylab as plt
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------    
# Compute product data class
class SaveProductData:
    
    #-------------------------------------------------------------------------------------
    # Init variable(s)
    sTimeNow = None
    
    oData = None
    oSettings = None
    oTime = None
    oGeoRef = None
    
    bFileAvailability = None
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method time info
    def __init__(self, sTimeNow, oData, oTime, oGeoRef, oSettings):
        
        # Saving global information
        self.sTimeNow = sTimeNow
        
        self.oData = oData
        self.oTime = oTime
        self.oGeoRef = oGeoRef
        self.oSettings = oSettings
            
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Creating product
    def SaveProduct(self):
        
        #-------------------------------------------------------------------------------------
        # Time now and product time
        sTimeNow = self.sTimeNow
        #sProductTime = self.sTimeNow[0:8]
        
        sFileNameRef = self.oSettings.sFileNameRef
        sDomainName = self.oSettings.sDomainName
        
        # Product name(s) and time
        sProductNameIN = self.oSettings.oDataSettings['Features']['ProductName']['NameIN']
        sProductNameOUT = self.oSettings.oDataSettings['Features']['ProductName']['NameOUT']
        sProductTimeFormatOUT = self.oSettings.oDataSettings['Features']['ProductTime']['TimeFormatOUT']
        
        # FileName 
        sFileNameOUT = self.oSettings.sFileNameOUT
        sFileNameOUT = sFileNameOUT.replace('product', sProductNameOUT)
        sFileNameOUT = sFileNameOUT.replace('yyyymmdd', sTimeNow[0:8])
        sFileNameOUT = sFileNameOUT.replace('HHMMSS', sTimeNow[8:14])
        
        # Source data path
        sPathDataDynamicOutcomeStep = self.oSettings.sPathDataDynamicOutcomeStep
        #-------------------------------------------------------------------------------------
          
        #-------------------------------------------------------------------------------------
        # Checked data availability
        if self.oData:
            
            #-------------------------------------------------------------------------------------
            # Product field(s)
            a1oProductFields = self.oSettings.oDataSettings['Fields']
            
            # GeoBox info
            a2dGeoX = self.oGeoRef.oGeoData.a2dGeoX
            a2dGeoY = self.oGeoRef.oGeoData.a2dGeoY
            dGeoXMin = np.nanmin(a2dGeoX); dGeoXMax = np.nanmax(a2dGeoX)
            dGeoYMax = np.nanmax(a2dGeoY); dGeoYMin = np.nanmin(a2dGeoY)
            oGeoBox = [dGeoXMin, dGeoYMax, dGeoXMax, dGeoYMin]
            a1dGeoBox = np.around( oGeoBox, decimals=3)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Cycling on output filename(s)
            for sFileNameOUT in self.oData:
                
                #-------------------------------------------------------------------------------------
                # File information
                print(' -------> Saving file ' + sFileNameOUT + ' ... ')
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Checking outcome file availability
                if not (os.path.isfile(join(sPathDataDynamicOutcomeStep,sFileNameOUT)) ):
                    
                    #-------------------------------------------------------------------------------------
                    # Extracting first level variable(s)
                    if not 'one-layer' in self.oData[sFileNameOUT].keys():
                        
                        # Dynamic-Layer
                        sDictName = 'FileDate'
                        sDateInput = self.oData[sFileNameOUT][sDictName]
                        self.oData[sFileNameOUT].pop(sDictName, None)
                        
                        sDictName = 'FileNameOutcome'
                        sFileNameOutcome = self.oData[sFileNameOUT][sDictName]
                        self.oData[sFileNameOUT].pop(sDictName, None)
                        
                        sDictName = 'FileNameInput'
                        a1sFileNameInput = self.oData[sFileNameOUT][sDictName]
                        self.oData[sFileNameOUT].pop(sDictName, None)
                        
                        sDictName = 'DateStep'
                        sDateStep = self.oData[sFileNameOUT][sDictName]; sDateStep = sDateStep.replace('_','')
                        self.oData[sFileNameOUT].pop(sDictName, None)
                        
                        sDictName = 'ProductNameInput'
                        sProductNameInput = self.oData[sFileNameOUT][sDictName]
                        self.oData[sFileNameOUT].pop(sDictName, None)
                        
                        sDictName = 'ProductNameOutcome'
                        sProductNameOutcome = self.oData[sFileNameOUT][sDictName]
                        self.oData[sFileNameOUT].pop(sDictName, None)
                    else:
                        # One-Layer
                        sDictName = 'FileDate'
                        sDateInput = self.oData[sFileNameOUT][sDictName]
                        sDictName = 'FileNameOutcome'
                        sFileNameOutcome = self.oData[sFileNameOUT][sDictName]
                        sDictName = 'FileNameInput'
                        a1sFileNameInput = self.oData[sFileNameOUT][sDictName]
                        sDictName = 'DateStep'
                        sDateStep = self.oData[sFileNameOUT][sDictName]; sDateStep = sDateStep.replace('_','')
                        sDictName = 'ProductNameInput'
                        sProductNameInput = self.oData[sFileNameOUT][sDictName]
                        sDictName = 'ProductNameOutcome'
                        sProductNameOutcome = self.oData[sFileNameOUT][sDictName]

                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Opening saving fields of db file
                    oSaveDriver = SaveVarData.SaveVarData(join(self.oSettings.sPathDataDynamicOutcomeStep,sFileNameOutcome), self.oGeoRef)
                    
                    # Saving global attribute(s)
                    oSaveDriver.writeGlobalAttr(sDateStep,'DateStep')
                    oSaveDriver.writeGlobalAttr(sProductNameInput,'ProductNameInput')
                    oSaveDriver.writeGlobalAttr(sProductNameOutcome,'ProductNameOutcome')
                    oSaveDriver.writeGlobalAttr(sFileNameRef,'FileNameReference')
                    oSaveDriver.writeGlobalAttr(sDomainName.lower(),'DomainName')
                    
                    # Saving dataset(s)
                    oSaveDriver.writeVar1D(sFileNameOutcome, 'FileNameOutcome')
                    oSaveDriver.writeVar1D(a1sFileNameInput, 'FileNameInput')
                    oSaveDriver.writeVar1D(sDateInput, 'FileDate')
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Cycling on data fields (at the same temporal step) --> rain accumulated (example)
                    for sFieldNameOUT in self.oData[sFileNameOUT]:
                        
                        #-------------------------------------------------------------------------------------
                        # Check field(s) type
                        if not (sFieldNameOUT =='GeoX' or sFieldNameOUT =='GeoY'):
                            
                            #-------------------------------------------------------------------------------------
                            # Checking data availability
                            try: 
                            
                                #-------------------------------------------------------------------------------------
                                # Extracting second level variable(s)
                                oValue = self.oData[sFileNameOUT][sFieldNameOUT]['Data']
                                #-------------------------------------------------------------------------------------
    
                                #-------------------------------------------------------------------------------------
                                # Cycling on on second level variable(s) --> SnowCoverV, SnowCoverQ ...
                                for sProductField in oValue.keys():
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Defining variable name
                                    sVarName = a1oProductFields[sProductField]['NameOUT']
                                    sVarName =  sVarName.replace('HH', sFieldNameOUT)
                                    print(' ------> Saving ' + sVarName + ' dynamic variable ... ')
                                    #-------------------------------------------------------------------------------------
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Checking sVarName is in keys
                                    if any(sProductField in sStr for sStr in a1oProductFields.keys()):
                                        
                                        oVarAttrs = a1oProductFields[sProductField]['Attrs']
                                        oMethodSaveData = getattr(oSaveDriver, oVarAttrs['saving_method'] )
                                        
                                        # Debugging
                                        #a2dVarTest = oValue[sProductField]
                                        #plt.figure()
                                        #plt.imshow(a2dVarTest); plt.colorbar();
                                        #plt.show()
                                        
                                        # Defining variable attribute(s)
                                        sVarLongName = oVarAttrs['long_name']
                                        sVarLongName = sVarLongName.replace('HH', sFieldNameOUT)
                                        
                                        # Saving file workspace
                                        oMethodSaveData(oValue[sProductField], sVarName, a1dGeoBox,
                                        oVarAttrs['standard_name'], sVarLongName, 
                                        oVarAttrs['cell_method'], oVarAttrs['units'], oVarAttrs['coordinates'], 
                                        oVarAttrs['grid_mapping'], oVarAttrs['model_description'], oVarAttrs['model_name'], 
                                        oVarAttrs['time_interp'],oVarAttrs['spatial_interp'],oVarAttrs['saving_method'],
                                        oVarAttrs['palette'], oVarAttrs['nodata'])
                                        
                                        # Variable(s) info saving
                                        print(' ------> Saving ' + sVarName + ' dynamic variable ... OK')
                                        
                                    else:
                                        # Variable(s) info saving
                                        print(' ------> Saving ' + sVarName + ' dynamic variable ... SKIPPED')
                                        pass
                                    #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                
                            except:
                                
                                #-------------------------------------------------------------------------------------
                                # Exit status field without 'data' 
                                pass
                                #-------------------------------------------------------------------------------------
                                
                            #-------------------------------------------------------------------------------------
                            
                        else:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit status for static fields in first variables level
                            pass
                            #-------------------------------------------------------------------------------------
                            
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Closing database file 
                    oSaveDriver.closeFile()
                    
                    # File information
                    print(' -------> Saving file ' + sFileNameOUT + ' ... OK')
                    #-------------------------------------------------------------------------------------
            
                else:
                    
                    #-------------------------------------------------------------------------------------
                    # File created previously exit status
                    print(' -------> Saving file ' + sFileNameOUT + ' ... File created previously')
                    #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
        else:
            
            #-------------------------------------------------------------------------------------
            # NoData exit status
            print(' -------> ATTENTION: product data is not available!')
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
            
    #-------------------------------------------------------------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
