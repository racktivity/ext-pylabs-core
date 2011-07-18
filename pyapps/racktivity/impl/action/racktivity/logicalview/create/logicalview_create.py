__author__ = 'racktivity'
__tags__ = 'logicalview', 'create'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #logicalview name already exists?
    if exists('view_logicalview_list', q.drp.logicalview, "name", params['name']):
        raise ValueError("Logicalview with name %s already exists"%params['name'])

    fields = ('name', 'description', 'viewstring', 'clouduserguid', 'share', 'tags')
    
    logicalview = q.drp.logicalview.new()
    for key, value in params.iteritems():
        if key in fields and value  != '':
            setattr(logicalview, key, value)
    acl = logicalview.acl.new()
    logicalview.acl = acl
    q.drp.logicalview.save(logicalview)
    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(logicalview.guid, 'logicalview', params['request']['username'])
    params['result'] = {'returncode': True,
                        'logicalviewguid': logicalview.guid}

def match(q, i, params, tags):
    return True
