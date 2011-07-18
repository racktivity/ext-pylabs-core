__author__ = 'racktivity'
__tags__ = 'row', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    row  = q.drp.row.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(row))

def match(q, i, params, tags):
    return True
