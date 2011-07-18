__author__ = 'racktivity'
__tags__ = 'datacenter', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    datacenter  = q.drp.datacenter.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(datacenter))

def match(q, i, params, tags):
    return True
