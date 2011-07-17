__author__ = 'racktivity'
__author__ = 'racktivity'
__tags__ = 'autodiscoverysnmpmap', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    autodiscoverysnmpmap  = q.drp.autodiscoverysnmpmap.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(autodiscoverysnmpmap))


def match(q, i, params, tags):
    return True


