__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.datacenter_find(name=params['name'], \
                                                                          description=params['description'], \
                                                                          locationguid=params['locationguid'], \
                                                                          clouduserguid=params['clouduserguid'],
                                                                          tags=params['tags'])}

def match(q, i, params, tags):
    return True
