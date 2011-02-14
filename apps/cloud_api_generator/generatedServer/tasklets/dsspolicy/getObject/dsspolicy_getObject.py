__author__ = 'aserver'
__tags__ = 'dsspolicy', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    dsspolicy  = q.drp.dsspolicy.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(dsspolicy))


def match(q, i, params, tags):
    return True


