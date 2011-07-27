__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = p.api.model.racktivity.clouduser.get(params['clouduserguid'])

def match(q, i, params, tags):
    return True

