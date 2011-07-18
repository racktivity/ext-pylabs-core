__author__ = 'racktivity'
__author__ = 'racktivity'
__tags__ = 'cable', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    cable  = q.drp.cable.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(cable))


def match(q, i, params, tags):
    return True


