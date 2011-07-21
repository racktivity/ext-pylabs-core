__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = p.api.model.racktivity.cloudusergroup.get(params['cloudusergroupguid'])
    membercloudusergroup = p.api.model.racktivity.cloudusergroup.get(params['membercloudusergroupguid'])
    if membercloudusergroup.guid in cloudusergroup.cloudusergroups:
        q.eventhandler.raiseError('Selected group is already part of the group')
    else:
        cloudusergroup.cloudusergroups.append(params['membercloudusergroupguid'])
        p.api.model.racktivity.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
