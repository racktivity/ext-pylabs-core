__author__ = 'racktivity'
__tags__ = 'monitoringinfo', 'getObject'

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    acl  = q.drp.monitoringinfo.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(monitoringinfo))

def match(q, i, params, tags):
    return True


