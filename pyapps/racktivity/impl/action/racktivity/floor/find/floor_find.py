__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'retruncode': True,
                        'guidlist': rootobjectaction_find.floor_find(name=params['name'], \
                                                                    datacenterguid=params['datacenterguid'], \
                                                                    floor=params['floor'], \
                                                                    alias=params['alias'],
                                                                    tags=params['tags'])}

def match(q, i, params, tags):
    return True