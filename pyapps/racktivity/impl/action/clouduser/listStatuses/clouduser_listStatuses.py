__author__ = 'racktivity'
__tags__ = 'clouduser', 'listStatuses'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    params['result'] = {'returncode': True,
                        'statuses': q.enumerators.clouduserstatustype._pm_enumeration_items.keys()}

def match(q, i, params, tags):
    return True

