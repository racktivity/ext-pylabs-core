__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    enterprise  = p.api.model.racktivity.enterprise.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(enterprise))

def match(q, i, params, tags):
    return True
