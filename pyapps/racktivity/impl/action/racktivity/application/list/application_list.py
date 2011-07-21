__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'applicationinfo':rootobjectaction_list.application_list(deviceguid=params['deviceguid'], \
                                                                                                     meteringdeviceguid=params['meteringdeviceguid'], \
                                                                                                     applicationguid=params['applicationguid'], \
                                                                                                     name=params['name'], \
                                                                                                     status=params['status'])}

def match(q, i, params, tags):
    return True
