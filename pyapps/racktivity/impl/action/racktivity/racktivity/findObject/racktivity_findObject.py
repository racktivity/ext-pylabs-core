__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    filterobj = p.api.model.racktivity.racktivity.getFilterObject()
    
    guids = p.api.model.racktivity.racktivity.find(filterobj)
    if guids:
        params['result'] = {'returncode': True,
                            'guid': guids[0]}
    else:
        params['result'] = {'returncode': False,
                            'guid': None}

def match(q, i, params, tags):
    return True
