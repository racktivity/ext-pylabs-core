__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = p.api.model.racktivity.cloudusergroup.get(params['cloudusergroupguid'])
    if params['clouduserguid'] in cloudusergroup.cloudusers:
        cloudusergroup.cloudusers.remove(params['clouduserguid'])
        p.api.model.racktivity.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode': True}
    else:
        q.logger.log('clouduserguid "%s" already removed' % params['clouduserguid'], 3)

def match(q, i, params, tags):
    return True

