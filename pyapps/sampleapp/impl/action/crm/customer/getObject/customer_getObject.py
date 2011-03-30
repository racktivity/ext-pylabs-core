__author__ = 'incubaid'
__tags__ = 'customer', 'get'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    
    customer = p.api.model.crm.customer.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(activity))

def match(q, i, p, params, tags):
    return True