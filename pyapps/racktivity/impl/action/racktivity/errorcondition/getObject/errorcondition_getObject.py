__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    errorcondition  = p.api.model.racktivity.errorcondition.get(params['errorconditionguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(errorcondition))

def match(q, i, params, tags):
    return True
