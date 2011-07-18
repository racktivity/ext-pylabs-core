__author__ = 'racktivity'
__tags__ = 'lan', 'find'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    result = rootobjectaction_find.lan_find(backplaneguid=params['backplaneguid'], name=params['name'], \
                                            status=params['status'], startip=params['startip'], endip=params['endip'], \
                                            gateway=params['gateway'], managementflag=params['managementflag'], publicflag=params['publicflag'], \
                                            storageflag=params['storageflag'], network=params['network'], netmask=params['netmask'], \
                                            parentlanguid=params['parentlanguid'], vlantag=params['vlantag'], lantype=params['lantype'],
                                            dhcpflag=params['dhcpflag'], tags=params['tags'])

    params['result'] = {'returncode': True,
                        'guidlist': result}

def match(q, i, params, tags):
    return True
