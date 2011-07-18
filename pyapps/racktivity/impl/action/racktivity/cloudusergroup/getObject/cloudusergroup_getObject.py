__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'getObject'

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    cloudusergroup  = q.drp.cloudusergroup.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(cloudusergroup))

def match(q, i, params, tags):
    return True


