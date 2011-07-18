__author__ = 'racktivity'
__tags__ = 'customer', 'listGroups'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    customer = q.drp.customer.get(params['customerguid'])
    groups = list()
    for groupguid in customer.cloudusergroups:
        #q.drp.cloudusergroup.query('select guid, name, description from cloudusergroup.view_cloudusergroup_list where cloudusers contains %s')
        cloudusergroup = q.drp.cloudusergroup.get(groupguid)
        groups.append({'guid': groupguid, 'name': cloudusergroup.name, 'description': cloudusergroup.description})
    
    params['result'] = {'returncode': True,
                        'groupinfo': groups}
    
def match(q, i, params, tags):
    return True
