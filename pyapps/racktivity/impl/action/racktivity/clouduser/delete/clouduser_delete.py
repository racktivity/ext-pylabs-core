__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params, nameKey = "login")
    params['result'] = {'returncode':False}
    clouduserguid = params['clouduserguid'] 
    cloudusergroupguids = p.api.model.racktivity.cloudusergroup.find(q.drp.cloudusergroup.getFilterObject())

    for cugg in cloudusergroupguids:
        cloudusergroup = p.api.model.racktivity.cloudusergroup.get(cugg)
        if clouduserguid in cloudusergroup.cloudusers:
            cloudusergroup.cloudusers.remove(clouduserguid)
            p.api.model.racktivity.cloudusergroup.save(cloudusergroup)

    clouduser = p.api.model.racktivity.clouduser.get(clouduserguid)
    result = p.api.model.racktivity.clouduser.delete(clouduserguid)
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True

