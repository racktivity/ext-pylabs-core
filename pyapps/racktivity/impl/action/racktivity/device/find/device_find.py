__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.device_find(name=params['name'], macaddress=params['macaddress'], \
                                                                      cableguid=params['cableguid'], status=params['status'], devicetype=params['devicetype'], \
                                                                      description=params['description'], template=params['template'], \
                                                                      modelnr=params['modelnr'], serialnr=params['serialnr'], firmware=params['firmware'], \
                                                                      rackguid=params['rackguid'], datacenterguid=params['datacenterguid'], \
                                                                      parentdeviceguid=params['parentdeviceguid'], tags=params['tags'])}

def match(q, i, params, tags):
    return True
