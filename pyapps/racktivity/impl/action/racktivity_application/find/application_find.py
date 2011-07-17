__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'find'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] =  {'returncode':True, 'guidlist': rootobjectaction_find.racktivity_application_find(deviceguid=params['deviceguid'], \
                                                                                                meteringdeviceguid=params['meteringdeviceguid'], \
                                                                                                istemplate=params['istemplate'], \
                                                                                                name=params['name'], \
                                                                                                status=params['status'],
                                                                                                tags=params['tags'])}

def match(q, i, params, tags):
    return True

