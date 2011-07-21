__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    enterprise = p.api.model.racktivity.enterprise.get(params['enterpriseguid'])
    
    if params['campus'] in enterprise.campuses:
        raise ValueError("Campus with guid %s already exists in the enterprise"%params['campus'])
    from rootobjectaction_lib import rootobjectaction_list
    if not rootobjectaction_list.location_list(params['campus']):
        raise ValueError("Campus with guid %s is not found in the system" % params['campus'])
    
    enterprise.campuses.append(params['campus'])
    p.api.model.racktivity.enterprise.save(enterprise)
    
    #import racktivityui.uigenerator.enterprise
    #racktivityui.uigenerator.enterprise.update()
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
