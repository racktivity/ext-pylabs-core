__author__ = 'racktivity'
__tags__ = 'enterprise', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    enterprise  = q.drp.enterprise.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(enterprise))

def match(q, i, params, tags):
    return True
