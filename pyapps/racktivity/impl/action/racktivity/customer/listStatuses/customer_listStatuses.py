__author__ = 'racktivity'
__tags__ = 'customer', 'listStatuses'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    params['result'] = {'returncode': True,
                        'statuses': q.enumerators.customerstatustype._pm_enumeration_items.keys()}

def match(q, i, params, tags):
    return True

