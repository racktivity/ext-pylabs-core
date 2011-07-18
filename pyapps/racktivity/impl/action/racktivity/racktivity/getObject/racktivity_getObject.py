__author__ = 'racktivity'
__tags__ = 'racktivity', 'getObject'

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    racktivity  = q.drp.racktivity.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(racktivity))

def match(q, i, params, tags):
    return True
