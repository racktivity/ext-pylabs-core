__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'listStatuses'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    res = q.enumerators.applicationstatustype._pm_enumeration_items.values()
    params['result'] = {'returncode':True, 'statustypes':res}

def match(q, i, params, tags):
    return True

