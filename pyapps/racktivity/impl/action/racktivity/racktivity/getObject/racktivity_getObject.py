__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = p.api.model.racktivity.racktivity.get(params['racktivityguid'])

def match(q, i, params, tags):
    return True

