__author__ = 'aserver'
__tags__ = 'machine', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    machine  = q.drp.machine.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(machine))


def match(q, i, params, tags):
    return True


