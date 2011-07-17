__author__ = 'racktivity'
__tags__ = 'clouduser', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'clouduserinfo': rootobjectaction_list.clouduser_list(clouduserguid=params['clouduserguid'])}

def match(q, i, params, tags):
    return True
