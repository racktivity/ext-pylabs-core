__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'addUser'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = q.drp.cloudusergroup.get(params['cloudusergroupguid'])
    clouduser = q.drp.clouduser.get(params['clouduserguid'])
    if clouduser.guid in cloudusergroup.cloudusers:
        q.eventhandler.raiseError('User already in group')
    else:
        cloudusergroup.cloudusers.append(params['clouduserguid'])
        q.drp.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True

