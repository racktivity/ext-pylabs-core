__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'delete'
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    cloudusergroupguid = params['cloudusergroupguid']
    customerslist = rootobjectaction_find.customer_find()
    for customerguid in customerslist:
        customer = q.drp.customer.get(customerguid)
        customer.cloudusergroups.remove(cloudusergroupguid)
        q.drp.customer.save(customer)

    cloudusergroupguids = q.drp.cloudusergroup.find(q.drp.cloudusergroup.getFilterObject())
    for cugg in cloudusergroupguids:
        if cugg == cloudusergroupguid:
            continue
        cloudusergroup = q.drp.cloudusergroup.get(cugg)
        if cloudusergroupguid in cloudusergroup.cloudusergroups:
            cloudusergroup.cloudusergroups.remove(cloudusergroupguid)
            q.drp.cloudusergroup.save(cloudusergroup)

    result = q.drp.cloudusergroup.delete(cloudusergroupguid)
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True

