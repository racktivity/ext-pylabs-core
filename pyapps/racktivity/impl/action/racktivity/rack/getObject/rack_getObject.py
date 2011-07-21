__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    rack  = p.api.model.racktivity.rack.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(rack))

def match(q, i, params, tags):
    return True
