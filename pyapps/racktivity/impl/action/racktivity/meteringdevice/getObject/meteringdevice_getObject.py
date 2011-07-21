__author__ = 'racktivity'

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    meteringdevice  = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(meteringdevice))

def match(q, i, params, tags):
    return True
