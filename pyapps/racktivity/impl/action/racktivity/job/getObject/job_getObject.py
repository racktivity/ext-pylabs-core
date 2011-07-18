__author__ = 'racktivity'
__tags__ = 'job', 'getObject'
__priority__= 3

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    import base64
    job  = q.drp.job.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(ThriftSerializer.serialize(job))

def match(q, i, params, tags):
    return True
