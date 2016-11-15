#-------------------------------------------------------------------------------------
# Class Features
__author__ = 'fabio'
__date__ = '20140415'
__version__ = '1.0.0'
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Library
import numpy as np
import scipy.interpolate as si
import osgeo.gdal
import os

# Partial library
from copy import deepcopy

#import matplotlib.pylab as plt
#-------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------
# Class reading settings
class ElabVarData:

    #-------------------------------------------------------------------------------------
    # Init vars
    oDataGeoRef = None
    oSettings = None
    oDataProduct = None
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataGeoRef=None, oSettings=None):
        
        # Georef and settings
        self.oDataGeoRef = oDataGeoRef
        self.oSettings = oSettings
    #-------------------------------------------------------------------------------------
    
    
#     
    #-------------------------------------------------------------------------------------
    # Creating grid from points
    def interpPoint2Grid(self, oDataVar):
        
        # Retrivieng static information
        a2dGeoXRef = self.oDataGeoRef.oGeoData.a2dGeoX
        a2dGeoYRef = self.oDataGeoRef.oGeoData.a2dGeoY
        iColsRef = self.oDataGeoRef.oGeoData.iCols
        iRowsRef = self.oDataGeoRef.oGeoData.iRows
        
        sPathTemp = self.oSettings.sPathTemp
        
        dRadiusX = self.oSettings.dRadiusX
        dRadiusY = self.oSettings.dRadiusY
        
        a2bGeoDataFinite = self.oDataGeoRef.a2bGeoDataFinite
        a2bGeoDataNan = self.oDataGeoRef.a2bGeoDataNan
        
        dNoData = np.nan
        
        oGeoXVar = oDataVar.oDataProduct['GeoX']
        oGeoYVar = oDataVar.oDataProduct['GeoY']
        
        # Checking array dimensions number
        if oGeoXVar != None and oGeoXVar != None:
        
            if (len(oGeoXVar.shape) == 1):
                a1dGeoXVar = oGeoXVar
                a1dGeoYVar = oGeoYVar
            elif (len(oGeoXVar.shape) == 2):
                
                a1iGeoDims = oGeoXVar.shape
                
                a1dGeoXVar = np.reshape(oGeoXVar, (a1iGeoDims[0] * a1iGeoDims[1]))
                a1dGeoYVar = np.reshape(oGeoYVar, (a1iGeoDims[0] * a1iGeoDims[1]))
            
            sDate = oDataVar.oDataProduct['FileDate']
            
            # File and product names raw 
            sFileNameInput = oDataVar.oDataProduct['FileNameInput']
            sProductNameInput = oDataVar.oDataProduct['ProductNameInput']
    
            if a1dGeoYVar is not None and a1dGeoXVar is not None: 
                if a1dGeoXVar.shape[0] == a1dGeoYVar.shape[0]:
                    
                    dGeoXRefMin = np.min(a2dGeoXRef)
                    dGeoXRefMax = np.max(a2dGeoXRef)
                    dGeoYRefMin = np.min(a2dGeoYRef)
                    dGeoYRefMax = np.max(a2dGeoYRef)
                     
                    # Checking values on selected domain
                    a1iIndexSel = []
                    a1iIndexSel = np.nonzero(((a1dGeoXVar>=dGeoXRefMin) & (a1dGeoXVar<=dGeoXRefMax)) &
                                  ((a1dGeoYVar>=dGeoYRefMin) & (a1dGeoYVar<=dGeoYRefMax)))
                    a1iIndexSel = a1iIndexSel[0]
                
                else:
                    #print('geocoord are different shape ... stopped')
                    a1iIndexSel = None;
    
            else:
                #print('geocoords are unknown ... stopped')
                a1iIndexSel = None;
            
            # Ckecking on data quality
            if a1iIndexSel is not None:
                
                oDataInterp = {}
                a1oDataVar = oDataVar.oDataProduct['Data']    
                
                # Cycling on data variable(s)   
                for sDataVar in a1oDataVar:
                    #print(sDataVar)
                    
                    # Checking if data are available on domain
                    if len(a1iIndexSel > 0):
                        
                        sFileName = sFileNameInput.split('.')[0]
                        oDataVar = a1oDataVar[sDataVar];
                        
                        # Checking array dimensions number
                        if (len(oDataVar.shape) == 1):
                            a1dDataVar = oDataVar
                        elif (len(oDataVar.shape) == 2):
                            a1iDataDims = oDataVar.shape
                            a1dDataVar = np.reshape(oDataVar, (a1iDataDims[0] * a1iDataDims[1]))
    
                        a1dDataVarSel = []; a1dGeoXVarSel = []; a1dGeoYVarSel = [];
                        a1dDataVarSel = a1dDataVar[a1iIndexSel]
                        a1dGeoXVarSel = a1dGeoXVar[a1iIndexSel];
                        a1dGeoYVarSel = a1dGeoYVar[a1iIndexSel];
                        
                        a1dDataVarSel.shape[0]
                        
                        # Storing all data in one dataset
                        a2dDataSel = [];
                        a2dDataSel = np.zeros(shape = [a1dDataVarSel.shape[0], 3])            
                        a2dDataSel[:,0] = a1dGeoXVarSel
                        a2dDataSel[:,1] = a1dGeoYVarSel
                        a2dDataSel[:,2] = a1dDataVarSel
                        
                        sOption = ( '-a nearest:radius1=' + str(dRadiusX) + ':radius2=' + 
                                    str(dRadiusY) + ':angle=0.0:nodata=' + str(dNoData) );
                        

                        # Writing asci file with data selected values
                        os.chdir(sPathTemp)
                        sVarGeoX = 'GeoX'; sVarGeoY = 'GeoY'; sVarData = 'GeoData'; 
                        sFileNameCSV = sFileName + '.csv';
                        oFid = open(sFileNameCSV , 'w' )
                        oFid.write( sVarGeoX + ',' +  sVarGeoY + ',' + sVarData +'\n' )
                        np.savetxt(oFid, a2dDataSel, fmt='%10.4f', delimiter=',', newline='\n')
                        oFid.close()
                        
                        sFileNameVRT = sFileName + '.vrt';
                        oFileVRT = open(sFileNameVRT,'w')
                        oFileVRT.write('<OGRVRTDataSource>\n')
                        oFileVRT.write('    <OGRVRTLayer name="' + sFileNameCSV[: -4] + '">\n')
                        oFileVRT.write('        <SrcDataSource>' + sFileNameCSV + '</SrcDataSource>\n')
                        oFileVRT.write('    <GeometryType>wkbPoint</GeometryType>\n')
                        oFileVRT.write('    <LayerSRS>WGS84</LayerSRS>\n')
                        oFileVRT.write('    <GeometryField encoding="PointFromColumns" x="'+sVarGeoX+'" y="'+sVarGeoY+'" z="' + sVarData+ '"/>\n')
                        oFileVRT.write('    </OGRVRTLayer>\n')
                        oFileVRT.write('</OGRVRTDataSource>\n')
                        oFileVRT.close()
                
                        sFileNameTiff = sFileName + '.tif';
                        sLineCommand = ('gdal_grid -zfield "' + sVarData + '"  -txe ' + 
                                        str(dGeoXRefMin) + ' ' + str(dGeoXRefMax) + ' -tye ' + 
                                        str(dGeoYRefMin) + ' ' + str(dGeoYRefMax) + ' -a_srs EPSG:4326 ' + 
                                        sOption + ' -outsize ' + str(iColsRef) + ' ' + str(iRowsRef)  + 
                                        ' -of GTiff -ot Float64 -l '+ sFileNameCSV[: -4] + ' ' + 
                                        sFileNameVRT + ' ' + sFileNameTiff + ' --config GDAL_NUM_THREADS ALL_CPUS' )
                        #print(sLineCommand)
                        os.system(sLineCommand)
                
                        oFileTiff = osgeo.gdal.Open(sFileNameTiff)
                        a2dDataVarInterp = np.zeros((iRowsRef, iColsRef))
                        a2dDataVarInterp = oFileTiff.ReadAsArray()
                        a2dDataVarInterp = np.flipud(a2dDataVarInterp)
                        
                        # Checking interpolation values 
                        a2dDataVarInterp[np.where(a2bGeoDataNan == True)] = np.nan
                        
                        # Debugging
                        #plt.figure()
                        #plt.imshow(a2dDataVarInterp); plt.colorbar()
                        #plt.show()
                        
                        if np.any(a2dDataVarInterp<0) == True:
                            print('============> ATTENTION: some values less than 0 (Interp Point2Grid)')
                            a2dDataVarInterp[np.where(a2dDataVarInterp<0) == True] = 0
                        if np.any(a2dDataVarInterp>100) == True:
                            print('============> ATTENTION: some values greater than 100 (Interp Point2Grid)')
                            a2dDataVarInterp[np.where(a2dDataVarInterp>100)] = 100
                        
                        oDataInterp[sDataVar] = a2dDataVarInterp;
                        
                    else:
                        # Data are not available on domain
                        #print('data are not available on selected domain ... stopped')
                        a2dDataVarInterp = np.zeros((iRowsRef, iColsRef)); 
                        a2dDataVarInterp[:] = np.nan
                        oDataInterp[sDataVar] = a2dDataVarInterp
                        
            else:
                # Problems on data reading
                #print('data are unknown on selected domain ... stopped')
                oDataInterp = None
                
            # Saving in self structure
            oData = {}
            oData['GeoX'] = a2dGeoXRef
            oData['GeoY'] = a2dGeoYRef
            oData['FileNameInput'] = sFileNameInput
            oData['FileNameOutcome'] = None
            oData['Data'] = oDataInterp
            oData['FileDate'] = sDate
            oData['DateStep'] = sDate
            oData['ProductNameInput'] = sProductNameInput.upper()
            oData['ProductNameOutcome'] = None
            
        else:
            # Exit for data problems
            print('============> ATTENTION: all data are none! Data are not available!')
            oData = None

        self.oDataProduct = oData
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Regridding variable on reference
    def gridVar(self, oDataVar):
        
        # Reference gcoordinates
        a2dGeoXRef = self.oDataGeoRef.oGeoData.a2dGeoX
        a2dGeoYRef = self.oDataGeoRef.oGeoData.a2dGeoY
        a1iGeoDims = a2dGeoYRef.shape
        
        # Data coordinates and values
        a1dGeoXVar = oDataVar['GeoX'].ravel()
        a1dGeoYVar = oDataVar['GeoY'].ravel()
        a1oDataVar = oDataVar['Data']
        
        a1bDataFinite = np.where(np.isfinite(a1dGeoXVar))
        
        a1dGeoXVarSel = a1dGeoXVar[a1bDataFinite]
        a1dGeoYVarSel = a1dGeoYVar[a1bDataFinite] 
        
        # Date file
        sDate = oDataVar['FileDate']
        
        # File and product names raw 
        sFileNameInput = oDataVar['FileNameInput']
        sProductNameInput = oDataVar['ProductNameInput']
        
        # Cycling on variable(s)
        oDataVarInterp = {}
        for sNameVar in a1oDataVar:

            a1dDataVar = []; a2dDataVar = []
            a2dDataVar = a1oDataVar[sNameVar]
            a1dDataVar = a2dDataVar.ravel()
            a1dDataVarSel = a1dDataVar[a1bDataFinite]
            
            a2dDataVarInterp = np.zeros((a1iGeoDims[0],a1iGeoDims[1])); 
            a2dDataVarInterp = si.griddata(
                                           (a1dGeoXVarSel, a1dGeoYVarSel), a1dDataVarSel,
                                           (a2dGeoXRef, a2dGeoYRef), method='nearest', 
                                           fill_value = np.nan)  
                        
            oDataVarInterp[sNameVar] = a2dDataVarInterp
            
            # Debugging
            #plt.figure(1)
            #plt.imshow(a2dDataVarInterp); plt.colorbar();
            #plt.figure(2)
            #plt.imshow(a2dDataVar); plt.colorbar();
            #plt.show()
             
        # Saving in self structure
        oData = {}
        oData['GeoX'] = a2dGeoXRef
        oData['GeoY'] = a2dGeoYRef
        oData['FileNameInput'] = sFileNameInput
        oData['FileNameOutcome'] = None
        oData['Data'] = oDataVarInterp
        oData['FileDate'] = sDate
        oData['DateStep'] = sDate
        oData['ProductNameInput'] = sProductNameInput
        oData['ProductNameOutcome'] = None

        self.oDataProduct = oData
    #-------------------------------------------------------------------------------------
    

            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
