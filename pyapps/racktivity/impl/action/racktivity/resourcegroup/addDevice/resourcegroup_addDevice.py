__author__ = 'aserver'
__tags__ = 'resourcegroup', 'addDevice'
__priority__= 3

def main(q, i, params, tags):
    resourcegroup = q.drp.resourcegroup.get(params['resourcegroupguid'])
    if not params['deviceguid'] in resourcegroup.deviceguids:
        resourcegroup.deviceguids.append(params['deviceguid'])
    q.drp.resourcegroup.save(resourcegroup)
    params['result'] = True

def match(q, i, params, tags):
    return True
