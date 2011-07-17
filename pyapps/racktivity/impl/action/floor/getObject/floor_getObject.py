__author__ = 'racktivity'
__tags__ = 'floor', 'getObject'

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    room  = q.drp.floor.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(room))

def match(q, i, params, tags):
    return True
