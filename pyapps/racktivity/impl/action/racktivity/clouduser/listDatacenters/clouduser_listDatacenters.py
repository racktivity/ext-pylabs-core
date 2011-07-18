__author__ = 'racktivity'
__tags__ = 'clouduser', 'listDatacenters'
__priority__= 3
def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    
def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    if not exists('view_clouduser_list', q.drp.clouduser, "guid", params['clouduserguid']):
        raise ValueError("invalid guid for clouduser, guid doesn't exists")

    usr = q.drp.clouduser
    from rootobjectaction_lib import rootobjectaction_find
    datacenters = rootobjectaction_find.datacenter_find(clouduserguid=params['clouduserguid'])
    params['result'] = {'returncode': True,
                        'guidlist': datacenters}

def match(q, i, params, tags):
    return True
