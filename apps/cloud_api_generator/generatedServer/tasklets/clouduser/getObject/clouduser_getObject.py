__author__ = 'aserver'
__tags__ = 'clouduser', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    clouduser  = q.drp.clouduser.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(clouduser))


def match(q, i, params, tags):
    return True


