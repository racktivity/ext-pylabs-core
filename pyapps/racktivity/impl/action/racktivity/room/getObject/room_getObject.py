__author__ = 'racktivity'

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    room  = p.api.model.racktivity.room.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(room))

def match(q, i, params, tags):
    return True
