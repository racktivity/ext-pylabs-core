__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'retruncode': True,
                        'guidlist': rootobjectaction_find.find("room",
                                                                name=params['name'], \
                                                                description=params['description'], \
                                                                datacenterguid=params['datacenterguid'], \
                                                                floorguid=params['floorguid'], \
                                                                alias=params['alias'],
                                                                tags=params['tags'])}

def match(q, i, params, tags):
    return True
