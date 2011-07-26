__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    enterprise = p.api.model.racktivity.enterprise.get(params['enterpriseguid'])
    enterprise.campuses.remove(params['campus'])
    p.api.model.racktivity.enterprise.save(enterprise)

    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
