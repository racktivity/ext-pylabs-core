__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    clouduser = p.api.model.racktivity.clouduser.get(params['clouduserguid'])
    clouduser.status = params['status']
    p.api.model.racktivity.clouduser.save(clouduser)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True

