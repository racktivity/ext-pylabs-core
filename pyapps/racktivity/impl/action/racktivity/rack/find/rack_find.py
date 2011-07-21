__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.rack_find(name=params['name'], racktype=params['racktype'], \
                                                                    description=params['description'], roomguid=params['roomguid'], \
                                                                    floor=params['floor'], corridor=params['corridor'], \
                                                                    position=params['position'], height=params['height'],
                                                                    tags=params['tags'])}

def match(q, i, params, tags):
    return True
