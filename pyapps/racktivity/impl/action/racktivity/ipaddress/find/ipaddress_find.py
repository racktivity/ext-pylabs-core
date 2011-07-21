__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.ipaddress_find(name=params['name'], description=params['description'], address=params['address'], \
                                                                         netmask=params['netmask'], block=params['block'], iptype=params['iptype'], \
                                                                         ipversion=params['ipversion'], languid=params['languid'], \
                                                                         cloudspaceguid=params['cloudspaceguid'], virtual=params['virtual'],
                                                                         tags=params['tags'])}

def match(q, i, params, tags):
    return True
