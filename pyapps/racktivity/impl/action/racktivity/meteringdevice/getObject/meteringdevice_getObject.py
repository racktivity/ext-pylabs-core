__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])

def match(q, i, params, tags):
    return True

