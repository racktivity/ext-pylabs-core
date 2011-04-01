__author__ = 'Incubaid'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    
    activity = p.api.model.crm.activity.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(activity))

def match(q, i, p, params, tags):
    return True