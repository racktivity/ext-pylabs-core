__author__ = 'aserver'
__tags__ = 'resourcegroup', 'removeDevice'
__priority__= 3

def main(q, i, params, tags):
    resourcegroup = q.drp.resourcegroup.get(params['resourcegroupguid'])
    if params['deviceguid'] in resourcegroup.deviceguids:
        resourcegroup.deviceguids.remove(params['deviceguid'])
    q.drp.resourcegroup.save(resourcegroup)
    params['result'] = True

def match(q, i, params, tags):
    return True
