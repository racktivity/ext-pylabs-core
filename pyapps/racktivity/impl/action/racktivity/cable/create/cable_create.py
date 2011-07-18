__author__ = 'racktivity'
__tags__ = 'cable', 'create'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #Check if another cable with the same name already exist
    if exists('view_cable_list', q.drp.cable, "name", params['name']):
        raise ValueError("Cable with the same name already exists")

    cable = q.drp.cable.new()
    fields = ('name', 'cabletype', 'description', 'label', 'tags')
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(cable, key, value)
    acl = cable.acl.new()
    cable.acl = acl
    q.drp.cable.save(cable)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(cable.guid, 'cable', params['request']['username'])

    params['result'] = {'returncode':True, 'cableguid': cable.guid}

def match(q, i, params, tags):
    return True

