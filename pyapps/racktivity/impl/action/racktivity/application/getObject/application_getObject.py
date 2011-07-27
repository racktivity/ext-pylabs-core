__author__ = 'racktivity'
__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    application  = p.api.model.racktivity.application.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(application))


def match(q, i, params, tags):
    return True


