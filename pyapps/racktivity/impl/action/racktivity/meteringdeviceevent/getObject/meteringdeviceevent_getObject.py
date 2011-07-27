__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = p.api.model.racktivity.meteringdeviceevent.get(params['meteringdeviceeventguid'])

def match(q, i, params, tags):
    return True

