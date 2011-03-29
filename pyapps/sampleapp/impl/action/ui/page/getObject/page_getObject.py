__tags__ = 'page','getObject'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    
    page = p.api.model.ui.page.get(params['rootobjectguid'])
    params['result'] = base64.encodestring(page.serialize(ThriftSerializer))
    
def match(q, i, p, params, tags):
	return True