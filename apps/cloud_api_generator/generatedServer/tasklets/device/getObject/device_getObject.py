__author__ = 'aserver'
__tags__ = 'device', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    device  = q.drp.device.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(device))


def match(q, i, params, tags):
    return True


