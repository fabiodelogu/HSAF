"""
Library Features:

Name:          Lib_Op_Exec_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160704'
Version:       '2.0.0'
"""

#######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

from Drv_Exception import Exc

import subprocess
import os

# Debug
# import matplotlib.pylab as plt
#######################################################################################

# -------------------------------------------------------------------------------------
# Method to run executable
def runExec(sCommandLine_EXEC=None, sPathName_EXEC=None, sRunName_EXEC='NoName'):

    # -------------------------------------------------------------------------------------
    # Info start
    oLogStream.info(' ====> RUN EXEC ... ')
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Check executable and command line
    try:

        # -------------------------------------------------------------------------------------
        # Info command line
        oLogStream.info(' -----> Run Name: ' + sRunName_EXEC)
        oLogStream.info(' -----> Command Line: ' + sCommandLine_EXEC)

        # Go to executable folder (if defined)
        if sPathName_EXEC:
            os.chdir(sPathName_EXEC)
        else:
            pass

        # Check command line definition
        if sCommandLine_EXEC:

            # Submit process
            oProcess = subprocess.Popen(sCommandLine_EXEC, shell=True, stdout=subprocess.PIPE)
            while True:
                sOut = oProcess.stdout.readline()
                if sOut == '' and oProcess.poll() is not None:

                    if oProcess.poll() == 0:
                        Exc.getExc(' -----> WARNING: RUN EXEC Process POOL = ' + str(oProcess.poll()), 2, 1)
                        sOut = 'RUN EXEC Process POOL Killed!'
                        oLogStream.info(str(sOut.strip()))
                        break
                    else:
                        Exc.getExc(' -----> ERROR: RUN EXEC failed! Check your settings!', 1, 1)
                if sOut:
                    oLogStream.info(str(sOut.strip()))

            # Collect stdout and stderr and exitcode
            sStdOut, sStdErr = oProcess.communicate()
            iStdCode = oProcess.poll()

            # Check process execution
            checkExec(sStdOut, sStdErr)

            # Info end
            oLogStream.info(' ====> RUN EXEC ... OK')
            return sStdOut, sStdErr, iStdCode

        else:
            # Exit info
            Exc.getExc(' -----> ERROR: RUN EXEC failed! Command line is not defined!', 1, 1)
        # -------------------------------------------------------------------------------------

    except subprocess.CalledProcessError:

        # -------------------------------------------------------------------------------------
        # Exit code for process error
        Exc.getExc(' -----> ERROR: RUN EXEC failed! Errors in the called executable!', 1, 1)
        # -------------------------------------------------------------------------------------

    except OSError:

        # -------------------------------------------------------------------------------------
        # Exit code for os error
        Exc.getExc(' -----> ERROR: RUN EXEC failed! Executable not found!', 1, 2)
        # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Check execution exit code
def checkExec(sOut=None, sErr=None):

    if (sOut is None or sOut == '') and sErr is None:
        pass
    else:
        Exc.getExc(' -----> WARNING: error occurred during RUN EXEC!', 2, 1)
    return
# -------------------------------------------------------------------------------------
