__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'cloudusergroupinfo': rootobjectaction_list.cloudusergroup_list(customerguid=params['customerguid'], \
                                                                                        cloudusergroupguid=params['cloudusergroupguid'])}

def match(q, i, params, tags):
    return True
