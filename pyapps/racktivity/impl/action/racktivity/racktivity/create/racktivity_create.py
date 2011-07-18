__author__ = 'racktivity'
__tags__ = 'racktivity', 'create'
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params, nameKey = "sw_version")
    params['result'] = {'returncode':False}
    racktivity = q.drp.racktivity.new()
    fields = ('sw_version', 'smtp', 'smtplogin', 'smtppassword', 'configured', 'tags')
    for key, value in params.iteritems():
        if key in fields and value not in ['', None]:
            setattr(racktivity, key, value)
    acl = racktivity.acl.new()
    racktivity.acl = acl
    q.drp.racktivity.save(racktivity)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(racktivity.guid, 'racktivity', params['request']['username'])

    params['result'] = {'returncode': True, 'racktivityguid': racktivity.guid}

def match(q, i, params, tags):
    return True