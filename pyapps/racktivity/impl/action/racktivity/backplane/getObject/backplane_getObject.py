__author__ = 'racktivity'
__tags__ = 'backplane', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    backplane  = q.drp.backplane.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(backplane))

def match(q, i, params, tags):
    return True
