__author__ = 'racktivity'
__priority__= 3
def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    
def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    if not exists('racktivity_view_clouduser_list', p.api.model.racktivity.clouduser, "guid", params['clouduserguid']):
        raise ValueError("invalid guid for clouduser, guid doesn't exists")

    usr = p.api.model.racktivity.clouduser
    from rootobjectaction_lib import rootobjectaction_find
    datacenters = rootobjectaction_find.datacenter_find(clouduserguid=params['clouduserguid'])
    params['result'] = {'returncode': True,
                        'guidlist': datacenters}

def match(q, i, params, tags):
    return True
