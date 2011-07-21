__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    row  = p.api.model.racktivity.row.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(row))

def match(q, i, params, tags):
    return True
