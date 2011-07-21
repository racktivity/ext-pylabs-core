__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    customer  = p.api.model.racktivity.customer.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(customer))


def match(q, i, params, tags):
    return True


