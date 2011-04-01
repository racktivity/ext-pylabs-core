__author__ = 'incubaid'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    
    customer = p.api.model.crm.customer.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(customer))

def match(q, i, p, params, tags):
    return True
