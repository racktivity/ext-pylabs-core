__author__ = 'racktivity'
__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    racktivity_application  = q.drp.racktivity_application.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(racktivity_application))


def match(q, i, params, tags):
    return True


