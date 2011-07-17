__author__ = 'racktivity'
__tags__ = 'ipaddress', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    ipaddress  = q.drp.ipaddress.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(ipaddress))

def match(q, i, params, tags):
    return True


