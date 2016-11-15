"""
Class Features

Name:          GetException
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160701'
Version:       '2.0.0'

Example:

import logging                                           # import logging library
oLogStream = logging.getLogger('sLogger')
from Drv_Exception import Exception                      # import Exception class

Exception(' -----> ERROR: test error!', 1, 1)            # error mode
Exception(' -----> WARNING: test warning!', 2, 1)        # warning mode
Exception('',0,0)                                        # no error mode
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')
######################################################################################

# -------------------------------------------------------------------------------------
# Class
class Exc:

    # -------------------------------------------------------------------------------------
    # Method init class
    def __init__(self):
        pass
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to get exception
    @classmethod
    def getExc(cls, sExcMessage, iExcType, iExcCode=None):

        # Get global information
        cls.sExcMessage = sExcMessage
        cls.iExcType = iExcType
        cls.iExcCode = iExcCode

        if cls.iExcCode:
            cls.iExcCode = str(cls.iExcCode)
        else:
            cls.iExcCode = 'undefined'

        # Get Exception
        if cls.iExcType == 1:
            cls.__getError(cls.sExcMessage, cls.iExcCode)
        elif cls.iExcType == 2:
            cls.__getWarning(cls.sExcMessage)
        elif cls.iExcType == 3:
            cls.__getCritical()
        if cls.iExcType == 0:
            cls.__getNone()
        else:
            pass

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Get error
    @staticmethod
    def __getError(sExcMessage, iExcCode):
        
        # -------------------------------------------------------------------------------------
        # Library
        import traceback
        import sys
        
        from os.path import split
        # -------------------------------------------------------------------------------------
        
        # -------------------------------------------------------------------------------------
        # Get system information
        oExcType, oExcOBJ, oExcTB = sys.exc_info()
        
        sExpFileName = split(oExcTB.tb_frame.f_code.co_filename)[1]
        iExpFileLine = oExcTB.tb_lineno
 
        # Write EXC information on log
        oLogStream.info(sExcMessage)
        oLogStream.error('[EXC_FORMAT]: ' + str(traceback.format_exc()))
        oLogStream.error('[EXC_INFO]: ' + str(sys.exc_info()[0]))
        oLogStream.error('[EXC_CODE]: ' + str(iExcCode))
        oLogStream.error('[EXC_FILENAME]: ' + sExpFileName)
        oLogStream.error('[EXC_FILELINE]: ' + str(iExpFileLine))              
                         
        # Fatal Error --> Exit the program with 1      
        sys.exit(1)
        # -------------------------------------------------------------------------------------
        
    # -------------------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------------------
    # Get warning
    @staticmethod
    def __getWarning(sExcMessage):
        
        # -------------------------------------------------------------------------------------
        # Write WARNING information on log
        oLogStream.info(sExcMessage)
        oLogStream.warning(sExcMessage)
        # -------------------------------------------------------------------------------------
        
    # -------------------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------------------
    # Get critical
    @staticmethod
    def __getCritical():
    
        pass
    
    # -------------------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------------------
    # Get none
    @staticmethod
    def __getNone():
        
        # -------------------------------------------------------------------------------------
        # Library
        import sys
        # -------------------------------------------------------------------------------------
        
        # -------------------------------------------------------------------------------------
        # Write NO ERROR information on log
        oLogStream.info('[EXC_FORMAT]: None')
        oLogStream.info('[EXC_INFO]: None')
        oLogStream.info('[EXC_CODE]: None')   
        oLogStream.info('[EXC_FILENAME]: None')
        oLogStream.info('[EXC_FILELINE]: None')              
                         
        # No Error --> Exit the program with 0   
        sys.exit(0)
        # -------------------------------------------------------------------------------------
        
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
