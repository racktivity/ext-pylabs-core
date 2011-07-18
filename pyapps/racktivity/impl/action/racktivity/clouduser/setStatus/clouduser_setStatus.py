__author__ = 'racktivity'
__tags__ = 'clouduser', 'setStatus'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    clouduser = q.drp.clouduser.get(params['clouduserguid'])
    clouduser.status = params['status']
    q.drp.clouduser.save(clouduser)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True

