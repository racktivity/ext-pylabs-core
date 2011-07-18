__author__ = 'racktivity'
__tags__ = 'enterprise', 'removeCampus'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    enterprise = q.drp.enterprise.get(params['enterpriseguid'])
    enterprise.campuses.remove(params['campus'])
    q.drp.enterprise.save(enterprise)
    
    import racktivityui.uigenerator.enterprise
    racktivityui.uigenerator.enterprise.update()
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
