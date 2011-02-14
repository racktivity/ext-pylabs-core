__author__ = 'aserver'
__tags__ = 'drpdb', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    drpdb  = q.drp.drpdb.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(drpdb))


def match(q, i, params, tags):
    return True


