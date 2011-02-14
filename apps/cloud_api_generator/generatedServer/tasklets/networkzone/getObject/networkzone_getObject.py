__author__ = 'aserver'
__tags__ = 'networkzone', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    networkzone  = q.drp.networkzone.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(networkzone))


def match(q, i, params, tags):
    return True


