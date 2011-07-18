__author__ = 'racktivity'
__tags__= 'policy', 'getObject'
__priority__ = 3

def main(q,i,params,tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    policy = q.drp.policy.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(policy))

def match(q,i,params,tags):
    return True
