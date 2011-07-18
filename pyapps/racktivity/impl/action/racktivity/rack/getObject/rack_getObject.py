__author__ = 'racktivity'
__tags__ = 'rack', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    rack  = q.drp.rack.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(rack))

def match(q, i, params, tags):
    return True
