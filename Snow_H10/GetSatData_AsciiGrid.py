'''
Created on Aug 21, 2013

@author: fabio
'''
import numpy as np
import h5py
import os.path

from os.path import join

class GetSatData_AsciiGrid:

    a1dGeoSatX = None
    a1dGeoSatY = None
    a1bGeoNoData = None

    def __init__(self, sFileName = None):
    
        """
        :rtype :  object containing sat data information 
        """
        
        sFilePath, sFileName = os.path.split(sFileName)
        
        if sFileName.endswith('hdf5') or sFileName.endswith('H5'):
        
            # Opening file
            oFile = h5py.File(join(sFilePath,sFileName),'r')
            sFileName = oFile.filename
            
            # Extracting data 
            oDatasetName = oFile[str('coords')]
            
            # Data conversion and nodata value definition
            oData = oDatasetName.value
            a2dGeoCoord = oData.astype(float)
            
            a1dGeoX = a2dGeoCoord[0,:]; a1dGeoX = np.flipud(a1dGeoX)
            a1dGeoX[a1dGeoX>200] = np.nan
            a1dGeoY = a2dGeoCoord[1,:]; a1dGeoY = np.flipud(a1dGeoY)
            a1dGeoY[a1dGeoY>200] = np.nan
            
            a1bGeoNoData = (a1dGeoY>200)
        
        elif sFileName.endswith('txt'):
            
            a2dGeoCoord = np.loadtxt(join(sFilePath,sFileName))
            
            a1dGeoX = a2dGeoCoord[:,0]; a1dGeoX = np.flipud(a1dGeoX)
            a1dGeoX[a1dGeoX>200] = np.nan
            a1dGeoY = a2dGeoCoord[:,1]; a1dGeoY = np.flipud(a1dGeoY)
            a1dGeoY[a1dGeoY>200] = np.nan
    
            a1bGeoNoData = (a1dGeoY>200)
        
        self.a1dGeoSatX = a1dGeoX
        self.a1dGeoSatY = a1dGeoY
        self.a1bGeoNoData = a1bGeoNoData








