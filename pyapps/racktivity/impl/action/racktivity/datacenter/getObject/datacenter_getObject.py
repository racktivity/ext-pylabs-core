__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    datacenter  = p.api.model.racktivity.datacenter.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(datacenter))

def match(q, i, params, tags):
    return True
