"""
Class Features:

Name:          Drv_Analysis_Interpolation
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160705'
Version:       '2.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')
#################################################################################

# --------------------------------------------------------------------
# Arguments dictionary
args = dict(oGeoX_IN=None, oGeoY_IN=None, oGeoZ_IN=None, oData_IN=None,
            oGeoX_OUT=None, oGeoY_OUT=None, oGeoZ_OUT=None, oGeoNan_OUT=None,
            dNoData_OUT=None, a2iIndex_OUT=None, bGeoCut_OUT=None,
            dRadiusX_OUT=None, dRadiusY_OUT=None, dRadiusInfluence_OUT=None,
            iEPSGCode=None, sPathTemp=None, oDataAnalyzed=None)
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Function to configure argument(s)
def config_args(kwargs):
    for k, v in kwargs.iteritems():
        if k in args.keys():
            args[k] = kwargs[k]
        else:
            args[k] = None
    return args
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Class to drive, select and run method(s)
class Drv_Analysis(object):

    # ----------------------------------------------------------------------------
    # Initialize class
    def __init__(self, lib_method=None, init_method=None, **kwargs):

        # Variable(s)
        self.lib_method = lib_method
        self.init_method = init_method
        self.config_args = config_args(kwargs)

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Method to get function by name
    def get_func(self):

        if hasattr(self.lib_method, self.init_method):
            sel_method = getattr(self.lib_method, self.init_method)
        else:
            sel_method = None

        return sel_method

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Method to check function arguments
    def check_args(self, sel_method=None):

        from inspect import getargspec

        if sel_method:

            func_args = getargspec(sel_method)
            if func_args.defaults:
                default_args = zip(func_args.args[-len(func_args.defaults):], func_args.defaults)
            else:
                default_args = None
            ins_args = func_args.args

            if default_args:
                for arg in default_args:
                    if arg[0] in ins_args:
                        try:
                            ins_args.remove(arg[0])
                        except ValueError:
                            pass

                    else:
                        pass
            else:
                pass

            sel_args = {}
            for k, v in self.config_args.iteritems():
                if v is not None:
                    if k in ins_args:
                        sel_args[k] = self.config_args[k]
                    else:
                        if k in ins_args:
                            ins_args.remove(k)
                        else:
                            pass
                else:
                    pass

            if ins_args.__len__() != sel_args.__len__():
                sel_args = None
            else:
                pass
        else:
            sel_args = None

        return sel_args

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Method to run function
    @staticmethod
    def run_func(sel_method=None, sel_args=None, default=None):

        if default is None:
            default = {}

        if sel_method and sel_args:
            try:
                result = sel_method(**sel_args)
                return result
            except ValueError:
                return default
        else:
            return default

    # ----------------------------------------------------------------------------

# ---------------------------------------------------------------------
