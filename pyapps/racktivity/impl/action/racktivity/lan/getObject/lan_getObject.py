__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    lan  = p.api.model.racktivity.lan.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(lan))


def match(q, i, params, tags):
    return True


