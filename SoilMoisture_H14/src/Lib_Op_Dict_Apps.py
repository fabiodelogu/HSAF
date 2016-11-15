"""
Library Features:

Name:          Lib_Op_Dict_Apps
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160704'
Version:       '2.0.0'
"""

#######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

from Drv_Exception import Exc

# Debug
# import matplotlib.pylab as plt
#######################################################################################

# -------------------------------------------------------------------------------------
# Method to prepare dictionary single or multiple keys (in list format)
def prepareDictKey(ob_keys, sep_keys=''):
    try:
        if isinstance(ob_keys, str):
            if sep_keys:
                dict_keys = ob_keys.split(sep_keys)
            else:
                dict_keys = [ob_keys]
            return dict_keys
        elif isinstance(ob_keys, list):
            dict_keys = ob_keys
            return dict_keys
        else:
            Exc.getExc(' -----> ERROR: keys format unknown!', 1, 1)
    except:
        return None
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to get values into dictionary using single or multiple keys (in list format)
def lookupDictKey(dic, key, *keys):
    try:
        if keys:
            return lookupDictKey(dic.get(key, {}), *keys)
        return dic.get(key)
    except:
        Exc.getExc(' -----> WARNING: impossible to get dictionary value using selected keys!', 2, 1)
        return None
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Delete key(s) from dictionary
def removeDictKeys(d, keys):

    if isinstance(keys, list):
        r = dict(d)
        for key in keys:
            if key in d:
                del r[key]
            else:
                pass
        return r
    else:
        Exc.getExc(' -----> WARNING: keys values must be included in a list!', 2, 1)
        return None
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Delete key from dictionary
def removeDictKey(d, key):
    if key in d:
        r = dict(d)
        del r[key]
        return r
    else:
        return d
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to get dictionary key recursively
def getDictKeyRecursive(search_dict, field):
    """Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.iteritems():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = getDictKeyRecursive(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = getDictKeyRecursive(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Get dictionary index using a selected key
def getDictIndex(dictionary=None, keyname=None):
    if dictionary and keyname:
        dict_keys = dictionary.keys()
        key_index = dict_keys.index(keyname)
    else:
        key_index= None
    return key_index
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Get selected index tuple from dictionary
def getDictTuple(dictionary=None, index=-1):    # considering development using scalar and array
    dict_sel = {}
    if dictionary and index >= 0:
        dict_tuple = dictionary.items()[index]
        dict_sel[dict_tuple[0]] = dict_tuple[1]
    else:
        dict_sel = None
    return dict_sel
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Get values from keys dictionary
def getDictSubKey(dictionary, *keys):
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Get keys from dictionary
def getDictKey(dataDict, mapList):
    return reduce(lambda d, k: d[k], mapList, dataDict)
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Method to join 2 dictionaries
def joinDict(oDictA=None, oDictB=None):
    if oDictA and oDictB:
        from copy import deepcopy
        oDictAB = deepcopy(oDictA)
        oDictAB.update(oDictB)
    else:
        oDictAB = None
    return oDictAB
# -------------------------------------------------------------------------------------
