'''
Created on Aug 21, 2013

@author: mirko
'''
import ReadArcInfo
import numpy as np

class GeoData:
  dGeoYMin = 0.0
  dGeoXMin = 0.0
  dGeoYMax = 0.0
  dGeoXMax = 0.0
    
  dGeoYStep = 0.0
  dGeoXStep = 0.0
  
  iRows = 0
  iCols = 0

  a2dGeoX = None
  a2dGeoY = None
  
  def __init__(self, dGeoYMin, dGeoXMin, dGeoYMax, dGeoXMax, dGeoYStep, dGeoXStep, iRows, iCols):

    self.dGeoYMin = dGeoYMin
    self.dGeoXMin = dGeoXMin
    self.dGeoYMax = dGeoYMax
    self.dGeoXMax = dGeoXMax
    
    self.dGeoYStep = dGeoYStep
    self.dGeoXStep = dGeoXStep
    
    self.iRows = iRows
    self.iCols = iCols
    
    # Creating geox and geoy references
    a1dGeoX = np.arange(dGeoXMin, dGeoXMax + np.abs(dGeoXStep/2), np.abs(dGeoXStep), float)
    a1dGeoY = np.arange(dGeoYMin, dGeoYMax + np.abs(dGeoYStep/2), np.abs(dGeoYStep), float)
    
    self.a2dGeoX, self.a2dGeoY = np.meshgrid(a1dGeoX, a1dGeoY)
    self.a2dGeoY = np.flipud(self.a2dGeoY)


class GetGeoData_AsciiGrid:
    
  oGeoData = None
  a2dGeoData = None

  def __init__(self, sFilename = None):
    
    """

    :rtype :  object conteining geo data information 
    """
    dFileInfo, a2dGeoData = ReadArcInfo.read_ARCINFO_ASCII_grid(sFilename)
    
    self.a2dGeoData = a2dGeoData
    self.dNoData = dFileInfo[ReadArcInfo.K_NODATAVALUE]
    self.a2bGeoDataFinite = (self.a2dGeoData > 0)
    self.a2bGeoDataNan = (self.a2dGeoData <= 0)
    
    dGeoXMin = dFileInfo[ReadArcInfo.K_XLLCORNER]
    dGeoXStep = dFileInfo[ReadArcInfo.K_CELLSIZE]
    dGeoYMin = dFileInfo[ReadArcInfo.K_YLLCORNER]
    dGeoYStep = dFileInfo[ReadArcInfo.K_CELLSIZE]
    
    iRows = dFileInfo[ReadArcInfo.K_NROWS]
    iCols = dFileInfo[ReadArcInfo.K_NCOLS]
    
    #coordinate del centro cella dello spigolo in alto a destra
    dGeoXMin = dGeoXMin + dGeoXStep/2.
    dGeoYMin = dGeoYMin + dGeoYStep/2.
    dGeoXMax = dGeoXMin + (iCols-1) * dGeoXStep
    dGeoYMax = dGeoYMin + (iRows-1) * dGeoYStep
    
    self.oGeoData = GeoData(dGeoYMin, dGeoXMin, dGeoYMax, dGeoXMax, dGeoYStep, dGeoXStep, iRows, iCols)

