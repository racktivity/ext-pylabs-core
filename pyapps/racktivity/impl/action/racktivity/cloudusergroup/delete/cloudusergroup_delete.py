__author__ = 'racktivity'
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    cloudusergroupguid = params['cloudusergroupguid']
    customerslist = rootobjectaction_find.customer_find()
    for customerguid in customerslist:
        customer = p.api.model.racktivity.customer.get(customerguid)
        customer.cloudusergroups.remove(cloudusergroupguid)
        p.api.model.racktivity.customer.save(customer)

    cloudusergroupguids = p.api.model.racktivity.cloudusergroup.find(q.drp.cloudusergroup.getFilterObject())
    for cugg in cloudusergroupguids:
        if cugg == cloudusergroupguid:
            continue
        cloudusergroup = p.api.model.racktivity.cloudusergroup.get(cugg)
        if cloudusergroupguid in cloudusergroup.cloudusergroups:
            cloudusergroup.cloudusergroups.remove(cloudusergroupguid)
            p.api.model.racktivity.cloudusergroup.save(cloudusergroup)

    result = p.api.model.racktivity.cloudusergroup.delete(cloudusergroupguid)
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True

