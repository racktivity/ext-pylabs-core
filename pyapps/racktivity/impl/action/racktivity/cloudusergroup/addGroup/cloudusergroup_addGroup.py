__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'addGroup'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = q.drp.cloudusergroup.get(params['cloudusergroupguid'])
    membercloudusergroup = q.drp.cloudusergroup.get(params['membercloudusergroupguid'])
    if membercloudusergroup.guid in cloudusergroup.cloudusergroups:
        q.eventhandler.raiseError('Selected group is already part of the group')
    else:
        cloudusergroup.cloudusergroups.append(params['membercloudusergroupguid'])
        q.drp.cloudusergroup.save(cloudusergroup)
        params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
