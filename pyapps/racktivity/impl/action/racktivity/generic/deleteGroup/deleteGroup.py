__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from logger import logger
    from rootobjectaction_lib import rootobject_tree
    #logger.log_tasklet(tags, params)
    params['result'] = {'returncode':False}
    rootobject = getattr(p.api.model.racktivity, tags[0])
    rootobjectinstance = rootobject.get(params['rootobjectguid'])
    acl = rootobjectinstance.acl
    if not acl:
        q.logger.log('no acl object for the rootobject')
        return
    group = params['group']
    groupaction = None
    action = params['action']
    if action:
        groupaction = group+"_"+action
        if groupaction in acl.cloudusergroupactions:
            del acl.cloudusergroupactions[groupaction]
        else:
            q.logger.log("group/action %s/%s doesn't exist, deleteGroup has no effect"%(group, action))
    else:
        #action is empty
        newgroupactions = dict()
        for key in acl.cloudusergroupactions.keys():
            if group != key.split('_')[0]:
                newgroupactions[key] = ''
        del acl.cloudusergroupactions
        acl.cloudusergroupactions = newgroupactions

    rootobject.save(rootobjectinstance)
    params['result'] = {'returncode':True}
    if params["recursive"]:
        children = rootobject_tree.getTree(params['rootobjectguid'], 1)["children"]
        for child in children:
            obj = getattr(p.api.action.racktivity, child["type"])
            obj.deleteGroup(rootobjectguid = child["guid"], group = group, action=action, recursive=True, request = params["request"])


def match(q, i, params, tags):
    return True
