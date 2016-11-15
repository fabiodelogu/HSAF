"""
Library Features:

Name:          Lib_Analysis_Computation
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160713'
Version:       '2.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

from Drv_Exception import Exc

# Debug
#import matplotlib.pylab as plt
#################################################################################

# --------------------------------------------------------------------------------
# Filter variable using a uniform area
def computeVarUnifArea(a2dVarData, iPixelSize=0, sFilterMode='nearest'):
    # Library
    from scipy import ndimage
    # Compute filter
    a2dVarFilter = ndimage.uniform_filter(a2dVarData, size=iPixelSize, mode=sFilterMode)
    # Return value
    return a2dVarFilter
# -------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Method to compute data kernel (snow)
def computeVarKernel(oDataGeo, a1iXIndex, a1iYIndex, dRadiusSnowInt):

    # -------------------------------------------------------------------------------------
    # NB: dRadiusSnowInt [km]
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Get static information
    a2dGeoData = oDataGeo.a2dGeoData
    a2dGeoX = oDataGeo.oGeoData.a2dGeoX
    a2dGeoY = oDataGeo.oGeoData.a2dGeoY
    dGeoXCellSize = oDataGeo.oGeoData.dGeoXStep
    dGeoYCellSize = oDataGeo.oGeoData.dGeoYStep
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Dynamic values (NEW)
    dR = 6378388  # (Radius)
    dE = 0.00672267  # (Ellipsoid)

    # dx = (R * cos(lat)) / (sqrt(1 - e2 * sqr(sin(lat)))) * PI / 180
    a2dDX = (dR * np.cos(a2dGeoY * np.pi / 180)) / (
    np.sqrt(1 - dE * np.sqrt(np.sin(a2dGeoY * np.pi / 180)))) * np.pi / 180
    # dy = (R * (1 - e2)) / pow((1 - e2 * sqr(sin(lat))),1.5) * PI / 180
    a2dDY = (dR * (1 - dE)) / np.power((1 - dE * np.sqrt(np.sin(a2dGeoY / 180))), 1.5) * np.pi / 180

    # a2dGeoAreaKm = ((a2dDX/(1/dGeoXCellSize)) * (a2dDY/(1/dGeoYCellSize))) / 1000000 # [km^2]
    a2dGeoAreaM = ((a2dDX / (1 / dGeoXCellSize)) * (a2dDY / (1 / dGeoYCellSize)))  # [m^2]

    # Area, Mean Dx and Dy values (meters)
    # a2dData = a2dGeoAreaM
    dGeoAreaMetersDxMean = np.sqrt(np.nanmean(a2dGeoAreaM))
    dGeoAreaMetersDyMean = np.sqrt(np.nanmean(a2dGeoAreaM))

    dGeoAreaMetersMean = np.mean([dGeoAreaMetersDxMean, dGeoAreaMetersDyMean])
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Pixel(s) snow interpolation
    iPixelSnowInt = np.int32(dRadiusSnowInt * 1000 / dGeoAreaMetersMean)
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Compute gridded indexes
    a1iX = np.linspace(0, a2dGeoData.shape[1], a2dGeoData.shape[1])
    a1iY = np.linspace(0, a2dGeoData.shape[0], a2dGeoData.shape[0])
    a2iX, a2iY = np.meshgrid(a1iX, a1iY)
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Cycle(s) on snow sensor(s)
    a2dW = np.zeros([a2dGeoData.shape[0], a2dGeoData.shape[1]])
    for iP in range(0, len(a1iXIndex)):
        # --------------------------------------------------------------------------------
        # Compute distance index matrix
        a2dDIndex = np.zeros([a2dGeoData.shape[0], a2dGeoData.shape[1]])
        a2dDIndex = np.sqrt((a2iY - a1iYIndex[iP]) ** 2 + (a2iX - a1iXIndex[iP]) ** 2)
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # Weight(s) matrix
        a2iIndex = np.zeros([a2dGeoData.shape[0], a2dGeoData.shape[1]])
        a2iIndex = np.where(a2dDIndex < iPixelSnowInt)
        a2dW[a2iIndex] = a2dW[a2iIndex] + (iPixelSnowInt ** 2 - a2dDIndex[a2iIndex] ** 2) / (
        iPixelSnowInt ** 2 + a2dDIndex[a2iIndex] ** 2) / len(a1iXIndex)
        # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Debug
    # plt.figure(1)
    # plt.imshow(a2dW); plt.colorbar();
    # plt.show()
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Return variable(s)
    return a2dW
    # --------------------------------------------------------------------------------


# --------------------------------------------------------------------------------
# Method to compute look-up table
def computeVarLUT(a2dVarData, a1oLookUpTable, sVarNameIN=None, sVarNameOUT=None):
    # Get data
    a2dVarData = np.float32(a2dVarData)
    # a2dVarTemp = deepcopy(a2dVarData)

    # Data final
    a2dVarFinal = np.zeros([a2dVarData.shape[0], a2dVarData.shape[1]]);

    # Check LUT availability
    if a1oLookUpTable:

        # Check if LUT is a dictionary
        if isinstance(a1oLookUpTable, dict):

            # Evalute LUT Key
            for sKeyLUT in a1oLookUpTable:

                # Extract LUT values
                oLookUpTable = a1oLookUpTable[sKeyLUT].values()

                if sVarNameIN:

                    oLookUpTable = a1oLookUpTable[sKeyLUT]

                    for sItem in oLookUpTable.keys():

                        if sItem == sVarNameIN:
                            oLUT_START = oLookUpTable[sVarNameIN]
                        else:
                            oLUT_END = oLookUpTable[sItem]
                            if not sVarNameOUT:
                                sVarNameOUT = sItem
                else:

                    oLookUpTable = a1oLookUpTable[sKeyLUT].values()
                    oLUT_START = oLookUpTable[0];
                    oLUT_END = oLookUpTable[1]

                # Check LUT format
                if isinstance(oLUT_START, list) and (isinstance(oLUT_END, int) or isinstance(oLUT_END, float)):

                    if len(oLUT_START) == 2:

                        dValueEnd = oLUT_END
                        oValueMin = oLUT_START[0];
                        oValueMax = oLUT_START[1]

                        if isinstance(oValueMin, int):
                            dValueStartMin = np.float32(oLUT_START[0])
                        elif isinstance(oValueMin, float):
                            dValueStartMin = np.float32(oLUT_START[0])
                        elif isinstance(oValueMin, str):
                            dValueStartMin = np.float32(oLUT_START[0])

                        if isinstance(oValueMax, int):
                            dValueStartMax = np.float32(oLUT_START[1])
                        elif isinstance(oValueMax, float):
                            dValueStartMax = np.float32(oLUT_START[1])
                        elif isinstance(oValueMax, str):
                            dValueStartMax = np.nan

                        # Assing value end
                        a2dVarFinal[(a2dVarData >= dValueStartMin) & (a2dVarData <= dValueStartMax)] = dValueEnd

                    else:
                        break

                elif isinstance(oLUT_START, int) and isinstance(oLUT_END, int):

                    dLUT_START = np.float32(oLUT_START);
                    dLUT_END = np.float32(oLUT_END);

                    if dLUT_START != dLUT_END:
                        a2dVarFinal[a2dVarData == dLUT_START] = dLUT_END
                    else:
                        pass

                else:
                    break
        else:
            pass
    else:
        pass

    # Debug data
    # plt.figure(1)
    # plt.imshow(a2dVarTemp); plt.colorbar(); plt.clim(100,255)
    # plt.figure(2)
    # plt.imshow(a2dVarData); plt.colorbar()
    # plt.figure(3)
    # plt.imshow(a2dVarFinal); plt.colorbar()
    # plt.show()

    return a2dVarFinal, sVarNameOUT

# --------------------------------------------------------------------------------
