__author__ = 'aserver'
__tags__ = 'vdc', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    vdc  = q.drp.vdc.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(vdc))


def match(q, i, params, tags):
    return True


