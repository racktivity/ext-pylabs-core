__author__ = 'racktivity'

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    racktivity  = p.api.model.racktivity.racktivity.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(racktivity))

def match(q, i, params, tags):
    return True
