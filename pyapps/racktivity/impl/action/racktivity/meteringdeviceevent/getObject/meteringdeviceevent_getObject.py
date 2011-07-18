__author__ = 'racktivity'
__tags__ = 'meteringdeviceevent', 'getObject'

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    event  = q.drp.meteringdeviceevent.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(event))

def match(q, i, params, tags):
    return True
