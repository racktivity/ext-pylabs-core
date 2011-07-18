__author__ = 'racktivity'
__tags__ = 'lan', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    lan  = q.drp.lan.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(lan))


def match(q, i, params, tags):
    return True


