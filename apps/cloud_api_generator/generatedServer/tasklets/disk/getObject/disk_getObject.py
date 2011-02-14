__author__ = 'aserver'
__tags__ = 'disk', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    disk  = q.drp.disk.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(disk))


def match(q, i, params, tags):
    return True


