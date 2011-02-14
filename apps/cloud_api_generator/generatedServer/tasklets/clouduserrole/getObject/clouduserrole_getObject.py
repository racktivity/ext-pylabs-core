__author__ = 'aserver'
__tags__ = 'clouduserrole', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    clouduserrole  = q.drp.clouduserrole.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(clouduserrole))


def match(q, i, params, tags):
    return True


