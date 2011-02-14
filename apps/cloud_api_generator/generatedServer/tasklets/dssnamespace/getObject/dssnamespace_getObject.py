__author__ = 'aserver'
__tags__ = 'dssnamespace', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    dssnamespace  = q.drp.dssnamespace.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(dssnamespace))


def match(q, i, params, tags):
    return True


