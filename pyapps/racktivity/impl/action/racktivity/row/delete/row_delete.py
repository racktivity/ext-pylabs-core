__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    rowguid = params["rowguid"]
    row = p.api.model.racktivity.row.get(rowguid)
    
    for rackguid in rootobjectaction_find.find("rack", rowguid=rowguid):
        p.api.action.racktivity.rack.delete(rackguid, request = params["request"])
        
    params['result'] = {'returncode': p.api.model.racktivity.row.delete(rowguid)}

    
    #Delete the policy linked to this roe
    q.logger.log('Deleting policies linked to this row', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=rowguid)
    for policyguid in  policyguids:
        p.api.model.racktivity.policy.delete(policyguid)

    #Delete the data stores linked to this row
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (rowguid, type))

    p.api.actor.racktivity.graphdatabase.destroyStores(databasenames)

def match(q, i, params, tags):
    return True
