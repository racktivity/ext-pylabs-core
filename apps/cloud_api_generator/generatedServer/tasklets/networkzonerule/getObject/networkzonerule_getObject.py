__author__ = 'aserver'
__tags__ = 'networkzonerule', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    networkzonerule  = q.drp.networkzonerule.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(networkzonerule))


def match(q, i, params, tags):
    return True


