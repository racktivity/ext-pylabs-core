__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'cloudusergroupinfo': rootobjectaction_list.cloudusergroup_list(customerguid=params['customerguid'], \
                                                                                        cloudusergroupguid=params['cloudusergroupguid'])}

def match(q, i, params, tags):
    return True
