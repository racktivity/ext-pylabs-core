__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    res =  q.enumerators.applicationaccounttype._pm_enumeration_items.values()
    params['result'] = {'returncode':True, 'accounttypes': res}

def match(q, i, params, tags):
    return True

