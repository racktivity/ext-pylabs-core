__author__ = 'aserver'
__author__ = 'aserver'
__tags__ = 'resourcegroup', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    resourcegroup  = q.drp.resourcegroup.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(resourcegroup))


def match(q, i, params, tags):
    return True


