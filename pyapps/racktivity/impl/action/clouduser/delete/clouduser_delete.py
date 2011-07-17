__author__ = 'racktivity'
__tags__ = 'clouduser', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params, nameKey = "login")
    params['result'] = {'returncode':False}
    clouduserguid = params['clouduserguid'] 
    cloudusergroupguids = q.drp.cloudusergroup.find(q.drp.cloudusergroup.getFilterObject())

    for cugg in cloudusergroupguids:
        cloudusergroup = q.drp.cloudusergroup.get(cugg)
        if clouduserguid in cloudusergroup.cloudusers:
            cloudusergroup.cloudusers.remove(clouduserguid)
            q.drp.cloudusergroup.save(cloudusergroup)

    clouduser = q.drp.clouduser.get(clouduserguid)
    result = q.drp.clouduser.delete(clouduserguid)
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True

