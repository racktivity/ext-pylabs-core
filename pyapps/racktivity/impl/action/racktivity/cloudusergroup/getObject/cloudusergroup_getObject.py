__author__ = 'racktivity'

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    cloudusergroup  = p.api.model.racktivity.cloudusergroup.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(cloudusergroup))

def match(q, i, params, tags):
    return True


