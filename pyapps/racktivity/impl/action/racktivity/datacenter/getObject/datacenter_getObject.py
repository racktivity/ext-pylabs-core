__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = p.api.model.racktivity.datacenter.get(params['datacenterguid'])

def match(q, i, params, tags):
    return True

