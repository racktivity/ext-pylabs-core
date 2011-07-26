__author__ = 'racktivity'
__priority__ = 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode': False}
    q.logger.log('Creating the new application in the model', 3)
    application = p.api.model.racktivity.application.new()
    fields = ('deviceguid', 'name', 'description', 'customsettings', 'parentapplicactionguid', 'meteringdeviceguid', 'template')

    for key, value in params.iteritems():
        if key in fields and value not in ['', None]:
            setattr(application, key, value)
    p.api.model.racktivity.application.save(application)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(application.guid, 'application', params['request']['username'])

    params['result'] = {'returncode':True, 'applicationguid':application.guid}

def match(q, i, params, tags):
    return True

