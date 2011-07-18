__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'applicationinfo':rootobjectaction_list.racktivity_application_list(deviceguid=params['deviceguid'], \
                                                                                                     meteringdeviceguid=params['meteringdeviceguid'], \
                                                                                                     applicationguid=params['applicationguid'], \
                                                                                                     name=params['name'], \
                                                                                                     status=params['status'])}

def match(q, i, params, tags):
    return True
