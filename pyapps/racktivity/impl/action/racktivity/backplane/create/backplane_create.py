__author__ = 'racktivity'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #Check if another backplane with the same name already exist
    if exists('racktivity_view_backplane_list', p.api.model.racktivity.backplane, "name", params['name']):
        raise ValueError("Backplane with the same name already exists")

    fields = ('name', 'backplanetype', 'description', 'publicflag', 'managementflag', 'storageflag', 'tags')
    backplane = p.api.model.racktivity.backplane.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(backplane, key, value)
    acl = backplane.acl.new()
    backplane.acl = acl
    p.api.model.racktivity.backplane.save(backplane)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(backplane.guid, 'backplane', params['request']['username'])

    params['result'] = {'returncode':True, 'backplaneguid':backplane.guid}

def match(q, i, params, tags):
    return True
