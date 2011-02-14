__author__ = 'aserver'
__tags__ = 'errorcondition', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    errorcondition  = q.drp.errorcondition.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(errorcondition))


def match(q, i, params, tags):
    return True


