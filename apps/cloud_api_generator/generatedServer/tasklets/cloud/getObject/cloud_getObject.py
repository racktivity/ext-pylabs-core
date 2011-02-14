__author__ = 'aserver'
__tags__ = 'cloud', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    cloud  = q.drp.cloud.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(cloud))


def match(q, i, params, tags):
    return True


