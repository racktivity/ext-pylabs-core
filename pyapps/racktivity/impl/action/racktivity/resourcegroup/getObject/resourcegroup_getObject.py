__author__ = 'aserver'
__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    resourcegroup  = p.api.model.racktivity.resourcegroup.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(resourcegroup))


def match(q, i, params, tags):
    return True


