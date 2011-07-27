__author__ = 'racktivity'

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    acl  = p.api.model.racktivity.monitoringinfo.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(monitoringinfo))

def match(q, i, params, tags):
    return True


