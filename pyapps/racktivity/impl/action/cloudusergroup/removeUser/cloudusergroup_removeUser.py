__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'removeUser'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = q.drp.cloudusergroup.get(params['cloudusergroupguid'])
    if params['clouduserguid'] in cloudusergroup.cloudusers:
        cloudusergroup.cloudusers.remove(params['clouduserguid'])
        q.drp.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode': True}
    else:
        q.logger.log('clouduserguid "%s" already removed' % params['clouduserguid'], 3)

def match(q, i, params, tags):
    return True

