__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = p.api.model.racktivity.cloudusergroup.get(params['cloudusergroupguid'])
    cloudusergroupguid = params['cloudusergroupguid']
    if cloudusergroupguid in cloudusergroup.cloudusergroupguids:
        cloudusergroup.cloudusergroups.remove(params['membercloudusergroupguid'])
        p.api.model.racktivity.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode': True}
    else:
        q.logger.log('cloudusergroup with guid "%s" already removed' % cloudusergroupguid, 3)

def match(q, i, params, tags):
    return True

