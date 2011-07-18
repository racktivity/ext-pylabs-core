__author__ = 'racktivity'
__tags__ = 'errorcondition', 'create'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    errorcondition = q.drp.errorcondition.new()
    keys = ('errorconditiontype', 'timestamp', 'level', 'agent', 'tags', 'errormessagepublic',
            'errormessageprivate', 'application', 'backtrace', 'logs', 'transactioninfo', 'tags')

    for key, value in params.iteritems():
        if key in keys and value:
            setattr(errorcondition, key, value)
    acl = errorcondition.acl.new()
    errorcondition.acl = acl
    q.drp.errorcondition.save(errorcondition)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(errorcondition.guid, 'errorcondition', params['request']['username'])

    params['result'] = {'returncode': True,
                        'errorconditionguid': errorcondition.guid} 

def match(q, i, params, tags):
    return True
