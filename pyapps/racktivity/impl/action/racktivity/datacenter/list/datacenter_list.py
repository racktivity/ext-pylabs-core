__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    datacenterguid = params['datacenterguid'] if 'datacenterguid' in params else None
    from rootobjectaction_lib import rootobjectaction_list
    datacenters = rootobjectaction_list.datacenter_list(datacenterguid=datacenterguid)
    params['result'] = {'returncode': True, 'datacenterinfo': datacenters}

def match(q, i, params, tags):
    return True
