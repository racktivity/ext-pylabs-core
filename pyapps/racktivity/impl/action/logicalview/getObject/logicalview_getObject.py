__author__ = 'racktivity'
__tags__ = 'logicalview', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    logicalview  = q.drp.logicalview.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(logicalview))

def match(q, i, params, tags):
    return True
