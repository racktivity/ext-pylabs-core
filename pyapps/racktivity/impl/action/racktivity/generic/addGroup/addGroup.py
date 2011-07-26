__author__ = 'racktivity'
__tags__ = ('application',
 'backplane',
 'cable',
 'clouduser',
 'cloudusergroup',
 'collector',
 'customer',
 'datacenter',
 'device',
 'enterprise',
 'errorcondition',
 'feed',
 'floor',
 'ipaddress',
 'job',
 'lan',
 'location',
 'logicalview',
 'meteringdevice',
 'meteringdeviceevent',
 'monitoringinfo',
 'pod',
 'policy',
 'rack',
 'racktivity',
 'racktivity_application',
 'resourcegroup',
 'room',
 'row',
 'threshold'), 'addGroup'
__priority__= 3


def main(q, i, p, params, tags):
    from logger import logger
    from rootobjectaction_lib import rootobject_tree
    #logger.log_tasklet(tags, params)
    q.logger.log('params='+str(params))
    q.logger.log('tags='+str(tags))
    params['result'] = {'returncode':False}
    rootobject = getattr(p.api.model.racktivity, tags[0])
    rootobjectinstance = rootobject.get(params['rootobjectguid'])

    group = params['group']
    groupaction = None
    action = params['action']
    actions = dir(getattr(p.api.action.racktivity, tags[0]))
    if action:
        if action not in actions:
            q.logger.log("action '%s' is not defined for root object"%action)
        groupaction = group+"_"+action
        rootobjectinstance.cloudusergroupactions[str(groupaction)] = ''
    else:
        #action is empty
        for methodname in actions:
            if not methodname.startswith('_'):
                rootobjectinstance.cloudusergroupactions[str(group+"_"+methodname)] = ''
    rootobject.save(rootobjectinstance)
    params['result'] = {'returncode':True}
    if params["recursive"]:
        children = rootobject_tree.getTree(params['rootobjectguid'], 1)["children"]
        for child in children:
            obj = getattr(p.api.action.racktivity, child["type"])
            obj.addGroup(rootobjectguid = child["guid"], group = group, action=action, recursive=True, request = params["request"])

def match(q, i, params, tags):
    return True
