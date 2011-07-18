__author__ = 'racktivity'
__tags__ = 'feed', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    feed  = q.drp.feed.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(feed))


def match(q, i, params, tags):
    return True


