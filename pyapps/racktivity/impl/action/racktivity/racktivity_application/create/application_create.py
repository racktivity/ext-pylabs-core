__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'create'
__priority__ = 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode': False}
    q.logger.log('Creating the new racktivity_application in the model', 3)
    racktivity_application = q.drp.racktivity_application.new()
    fields = ('deviceguid', 'name', 'description', 'customsettings', 'parentapplicactionguid', 'meteringdeviceguid', 'template')

    for key, value in params.iteritems():
        if key in fields and value not in ['', None]:
            setattr(racktivity_application, key, value)
    acl = racktivity_application.acl.new()
    racktivity_application.acl = acl
    q.drp.racktivity_application.save(racktivity_application)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(racktivity_application.guid, 'racktivity_application', params['request']['username'])

    params['result'] = {'returncode':True, 'applicationguid':racktivity_application.guid}

def match(q, i, params, tags):
    return True

