__author__ = 'racktivity'
__tags__ = 'pod', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    pod  = q.drp.pod.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(pod))

def match(q, i, params, tags):
    return True
