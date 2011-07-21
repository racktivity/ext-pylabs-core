__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    params['result'] = {'returncode': True,
                        'statuses': q.enumerators.customerstatustype._pm_enumeration_items.keys()}

def match(q, i, params, tags):
    return True

