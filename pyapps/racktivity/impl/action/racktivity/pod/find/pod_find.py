__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.pod_find(name=params['name'], alias=params['alias'], roomguid=params['roomguid'], \
                                                                   rackguid=params['rackguid'], tags=params['tags'])}

def match(q, i, params, tags):
    return True
