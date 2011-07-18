__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'create'
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    fields = ('name', 'description', 'tags')
    cloudusergroup = q.drp.cloudusergroup.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(cloudusergroup, key, value)
    acl = cloudusergroup.acl.new()
    cloudusergroup.acl = acl
    q.drp.cloudusergroup.save(cloudusergroup)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(cloudusergroup.guid, 'cloudusergroup', params['request']['username'])

    params['result'] = {'returncode': True,
                        'cloudusergroupguid': cloudusergroup.guid}

def match(q, i, params, tags):
    return True

