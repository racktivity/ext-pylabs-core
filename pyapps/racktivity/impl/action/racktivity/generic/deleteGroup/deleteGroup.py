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
 'threshold'), 'deleteGroup'
__priority__= 3

def main(q, i, p, params, tags):
    from logger import logger
    from rootobjectaction_lib import rootobject_tree
    #logger.log_tasklet(tags, params)
    params['result'] = {'returncode':False}
    rootobject = getattr(p.api.model.racktivity, tags[0])
    rootobjectinstance = rootobject.get(params['rootobjectguid'])

    group = params['group']
    groupaction = None
    action = params['action']
    if action:
        groupaction = group+"_"+action
        if groupaction in rootobjectinstance.cloudusergroupactions:
            del rootobjectinstance.cloudusergroupactions[groupaction]
        else:
            q.logger.log("group/action %s/%s doesn't exist, deleteGroup has no effect"%(group, action))
    else:
        #action is empty
        newgroupactions = dict()
        for key in rootobjectinstance.cloudusergroupactions.keys():
            if group != key.split('_')[0]:
                newgroupactions[key] = ''
        del rootobjectinstance.cloudusergroupactions
        rootobjectinstance.cloudusergroupactions = newgroupactions

    rootobject.save(rootobjectinstance)
    params['result'] = {'returncode':True}
    if params["recursive"]:
        children = rootobject_tree.getTree(params['rootobjectguid'], 1)["children"]
        for child in children:
            obj = getattr(p.api.action.racktivity, child["type"])
            obj.deleteGroup(rootobjectguid = child["guid"], group = group, action=action, recursive=True, request = params["request"])


def match(q, i, params, tags):
    return True
