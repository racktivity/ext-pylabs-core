__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    fields = ('name', 'description', 'tags')
    cloudusergroup = p.api.model.racktivity.cloudusergroup.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(cloudusergroup, key, value)
    acl = cloudusergroup.acl.new()
    cloudusergroup.acl = acl
    p.api.model.racktivity.cloudusergroup.save(cloudusergroup)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(cloudusergroup.guid, 'cloudusergroup', params['request']['username'])

    params['result'] = {'returncode': True,
                        'cloudusergroupguid': cloudusergroup.guid}

def match(q, i, params, tags):
    return True

