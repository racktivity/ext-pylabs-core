__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    location  = p.api.model.racktivity.location.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(location))

def match(q, i, params, tags):
    return True
