__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getObject'

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    meteringdevice  = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(meteringdevice))

def match(q, i, params, tags):
    return True
