__author__ = 'racktivity'
__tags__ = 'threshold', 'getObject'

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    threshold  = q.drp.threshold.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(threshold))

def match(q, i, params, tags):
    return True
