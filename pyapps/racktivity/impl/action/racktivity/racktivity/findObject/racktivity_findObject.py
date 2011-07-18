__author__ = 'racktivity'
__tags__ = 'racktivity', 'findObject'

def main(q, i, params, tags):
    params['result'] = {'returncode': False}
    filterobj = q.drp.racktivity.getFilterObject()
    
    guids = q.drp.racktivity.find(filterobj)
    if guids:
        params['result'] = {'returncode': True,
                            'guid': guids[0]}
    else:
        params['result'] = {'returncode': False,
                            'guid': None}

def match(q, i, params, tags):
    return True
