__author__ = 'racktivity'
__tags__ = 'location', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    location  = q.drp.location.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(location))

def match(q, i, params, tags):
    return True
