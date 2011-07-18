__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'removeGroup'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = q.drp.cloudusergroup.get(params['cloudusergroupguid'])
    cloudusergroupguid = params['cloudusergroupguid']
    if cloudusergroupguid in cloudusergroup.cloudusergroupguids:
        cloudusergroup.cloudusergroups.remove(params['membercloudusergroupguid'])
        q.drp.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode': True}
    else:
        q.logger.log('cloudusergroup with guid "%s" already removed' % cloudusergroupguid, 3)

def match(q, i, params, tags):
    return True

