__tags__ = 'pop3','create'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    
    pop3 = p.api.model.config.pop3.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(pop3.serialize(ThriftSerializer))
    
def match(q, i, p, params, tags):
	return True