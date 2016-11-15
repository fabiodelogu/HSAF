"""
Library Features:

Name:          Lib_File_Log_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160703'
Version:       '2.0.0'
"""

#################################################################################

#--------------------------------------------------------------------------------
# Method to get file history
def getFileHistory(sFileHistory):
    import csv
    from os.path import exists

    if exists(sFileHistory):
        oFileReader = csv.reader(open(sFileHistory, 'r'), delimiter=',')
        return zip(*oFileReader)
    else:
        return None
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method to write file history
def writeFileHistory(sFileHistory, oDataHistory):
    import csv
    with open(sFileHistory, 'wb') as oFile:
        oFileWriter = csv.writer(oFile, delimiter=',')
        oFileWriter.writerows(oDataHistory)
#--------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to check saving time of a file
def checkSavingTime(sTime, a1oTimeSteps, iTimeStep, iTimeUpd):

    # -------------------------------------------------------------------------------------
    # Library
    import datetime
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Saving condition (almost > 0)
    bSavingTime = False
    if iTimeUpd > 0:

        # -------------------------------------------------------------------------------------
        # Define timeto and timefrom (period)
        oTimeTo = datetime.datetime.strptime(a1oTimeSteps[-1], '%Y%m%d%H%M')
        oTimeFrom = oTimeTo - datetime.timedelta(seconds=int(iTimeStep) * int(iTimeUpd))

        # Define time
        oTime = datetime.datetime.strptime(sTime, '%Y%m%d%H%M')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Define file saving
        if (oTime >= oTimeFrom and oTime <= oTimeTo):
            bSavingTime = True
        else:
            bSavingTime = False
            # -------------------------------------------------------------------------------------

    elif iTimeUpd == 0:

        # -------------------------------------------------------------------------------------
        # Define timeto and timefrom (period)
        oTimeTo = datetime.datetime.strptime(a1oTimeSteps[-1], '%Y%m%d%H%M')
        # Define time
        oTime = datetime.datetime.strptime(sTime, '%Y%m%d%H%M')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Define file saving
        if (oTime == oTimeTo):
            bSavingTime = True
        else:
            bSavingTime = False
            # -------------------------------------------------------------------------------------

    elif iTimeUpd == -1:

        # -------------------------------------------------------------------------------------
        # Define file saving
        bSavingTime = False
        # -------------------------------------------------------------------------------------

    else:

        # -------------------------------------------------------------------------------------
        # Define file saving
        bSavingTime = False
        # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Return variable(s)
    return bSavingTime
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
