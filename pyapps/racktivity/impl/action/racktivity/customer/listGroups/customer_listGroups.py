__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    customer = p.api.model.racktivity.customer.get(params['customerguid'])
    groups = list()
    for groupguid in customer.cloudusergroups:
        #p.api.model.racktivity.cloudusergroup.query('select guid, name, description from cloudusergroup.view_cloudusergroup_list where cloudusers contains %s')
        cloudusergroup = p.api.model.racktivity.cloudusergroup.get(groupguid)
        groups.append({'guid': groupguid, 'name': cloudusergroup.name, 'description': cloudusergroup.description})
    
    params['result'] = {'returncode': True,
                        'groupinfo': groups}
    
def match(q, i, params, tags):
    return True
