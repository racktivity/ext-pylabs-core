__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = p.api.model.racktivity.pod.get(params['rootobjectguid'])

def match(q, i, params, tags):
    return True

