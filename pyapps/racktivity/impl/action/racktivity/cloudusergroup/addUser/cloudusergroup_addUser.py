__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = p.api.model.racktivity.cloudusergroup.get(params['cloudusergroupguid'])
    clouduser = p.api.model.racktivity.clouduser.get(params['clouduserguid'])
    if clouduser.guid in cloudusergroup.cloudusers:
        q.eventhandler.raiseError('User already in group')
    else:
        cloudusergroup.cloudusers.append(params['clouduserguid'])
        p.api.model.racktivity.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True

