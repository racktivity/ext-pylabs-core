__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find
def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params, nameKey = "login")
    params['result'] = {'returncode':False}
    if rootobjectaction_find.clouduser_find(login=params['login']):
        q.eventhandler.raiseError("Clouduser with login '%s' already exists"%params['login'])
    
    keys = ('login', 'password', 'email', 'firstname', 'lastname', 'name', 'description', 'tags')
    
    clouduser = p.api.model.racktivity.clouduser.new()
    for key, value in params.iteritems():
        if key in keys:
            setattr(clouduser, key, value)
    import enumerations
    clouduser.status = enumerations.clouduserstatustype.CREATED

    p.api.model.racktivity.clouduser.save(clouduser)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(clouduser.guid, 'clouduser', params['request']['username'])

    params['result'] = {'returncode': True,
                        'clouduserguid': clouduser.guid}

def match(q, i, params, tags):
    return True
