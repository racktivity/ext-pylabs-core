__author__ = 'racktivity'

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    threshold  = p.api.model.racktivity.threshold.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(threshold))

def match(q, i, params, tags):
    return True
