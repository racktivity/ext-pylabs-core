__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(tags, params)
    q.logger.log('params='+str(params))
    params['result'] = {'returncode':False}
    rootobject = getattr(p.api.model.racktivity, tags[0])
    rootobjectinstance = rootobject.get(params['rootobjectguid'])
    acl = rootobjectinstance.acl
    if not acl:
        acl = rootobjectinstance.acl.new()
        rootobjectinstance.acl = acl

    acl.cloudusergroupactions = params['cloudusergroupnames']
    rootobject.save(rootobjectinstance)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
