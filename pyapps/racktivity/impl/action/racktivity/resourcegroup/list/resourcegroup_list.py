__author__ = 'aserver'
__priority__= 3

from rootobjectaction_lib import rootobjectaction_list

def main(q, i, p, params, tags):
    params['result'] = {'returncode': True,
                        'resourcegroupinfo': rootobjectaction_list.resourcegroup_list(resourcegroupguid=params['resourcegroupguid'],
                                                     customerguid=params['customerguid'],
                                                     deviceguid=params['deviceguid'])}

def match(q, i, params, tags):
    return True

