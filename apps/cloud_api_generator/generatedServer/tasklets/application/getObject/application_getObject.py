__author__ = 'aserver'
__tags__ = 'application', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    application  = q.drp.application.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(application))


def match(q, i, params, tags):
    return True


