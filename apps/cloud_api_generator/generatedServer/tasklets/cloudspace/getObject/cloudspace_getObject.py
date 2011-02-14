__author__ = 'aserver'
__tags__ = 'cloudspace', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    cloudspace  = q.drp.cloudspace.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(cloudspace))


def match(q, i, params, tags):
    return True


