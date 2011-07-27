__author__ = 'racktivity'
__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    autodiscoverysnmpmap  = p.api.model.racktivity.autodiscoverysnmpmap.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(autodiscoverysnmpmap))


def match(q, i, params, tags):
    return True


