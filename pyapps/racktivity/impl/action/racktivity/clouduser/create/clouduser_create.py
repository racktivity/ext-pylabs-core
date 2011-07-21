__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params, nameKey = "login")
    params['result'] = {'returncode':False}
    cloudusers = p.api.model.racktivity.clouduser.findAsView(q.drp.clouduser.getFilterObject(),'racktivity_view_clouduser_list')
    if [cu for cu in cloudusers if cu['login'] == params['login']]:
        q.eventhandler.raiseError("Clouduser with login '%s' already exists"%params['login'])
        return
    
    keys = ('login', 'password', 'email', 'firstname', 'lastname', 'name', 'description', 'tags')
    
    clouduser = p.api.model.racktivity.clouduser.new()
    for key, value in params.iteritems():
        if key in keys:
            setattr(clouduser, key, value)
    
    clouduser.status = q.enumerators.clouduserstatustype.CREATED
    acl = clouduser.acl.new()
    clouduser.acl = acl
    p.api.model.racktivity.clouduser.save(clouduser)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(clouduser.guid, 'clouduser', params['request']['username'])

    params['result'] = {'returncode': True,
                        'clouduserguid': clouduser.guid}

def match(q, i, params, tags):
    return True
