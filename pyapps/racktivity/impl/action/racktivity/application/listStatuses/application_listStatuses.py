__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    res = q.enumerators.applicationstatustype._pm_enumeration_items.values()
    params['result'] = {'returncode':True, 'statustypes':res}

def match(q, i, params, tags):
    return True

