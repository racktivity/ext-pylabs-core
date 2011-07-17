__author__ = 'racktivity'
__tags__ = 'customer', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    customer  = q.drp.customer.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(customer))


def match(q, i, params, tags):
    return True


