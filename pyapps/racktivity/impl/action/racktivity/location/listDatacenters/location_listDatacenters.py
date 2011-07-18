__author__ = 'racktivity'
__tags__ = 'location', 'listDatacenters'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    if not q.drp.location.get(params['locationguid']):
        raise ValueError('Location with GUID %s does not exist'%params['locationguid'])
    params['result'] = {'returncode':True, 'guidlist':rootobjectaction_find.datacenter_find(locationguid=params['locationguid'])}
    

def match(q, i, params, tags):
    return True