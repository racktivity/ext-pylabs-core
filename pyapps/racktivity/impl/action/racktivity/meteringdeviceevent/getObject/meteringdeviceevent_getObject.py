__author__ = 'racktivity'

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    event  = p.api.model.racktivity.meteringdeviceevent.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(event))

def match(q, i, params, tags):
    return True
