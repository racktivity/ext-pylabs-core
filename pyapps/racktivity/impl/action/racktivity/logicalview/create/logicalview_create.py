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
    #logicalview name already exists?
    if exists('racktivity_view_logicalview_list', p.api.model.racktivity.logicalview, "name", params['name']):
        raise ValueError("Logicalview with name %s already exists"%params['name'])

    fields = ('name', 'description', 'viewstring', 'clouduserguid', 'share', 'tags')
    
    logicalview = p.api.model.racktivity.logicalview.new()
    for key, value in params.iteritems():
        if key in fields and value  != '':
            setattr(logicalview, key, value)
    acl = logicalview.acl.new()
    logicalview.acl = acl
    p.api.model.racktivity.logicalview.save(logicalview)
    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(logicalview.guid, 'logicalview', params['request']['username'])
    params['result'] = {'returncode': True,
                        'logicalviewguid': logicalview.guid}

def match(q, i, params, tags):
    return True
