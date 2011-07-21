__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(tags, params)
    params['result'] = {'returncode':False}
    rootobject = getattr(p.api.model.racktivity, tags[0])
    rootobjectinstance = rootobject.get(params['rootobjectguid'])
    acl = rootobjectinstance.acl
    if not acl:
        q.logger.log('no acl object for this rootobject')
        return
    groups = params['groups']
    action = params['action']
     
    for group in groups:
        groupaction = str(group + "_" + action)
        if groupaction in acl.cloudusergroupactions.keys():
         params['result'] = {'returncode':True}
         break

def match(q, i, params, tags):
    return True
