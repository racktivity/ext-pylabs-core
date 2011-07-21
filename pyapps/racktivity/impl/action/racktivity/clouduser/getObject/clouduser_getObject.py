__author__ = 'racktivity'
__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    clouduser  = p.api.model.racktivity.clouduser.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(clouduser))


def match(q, i, params, tags):
    return True


