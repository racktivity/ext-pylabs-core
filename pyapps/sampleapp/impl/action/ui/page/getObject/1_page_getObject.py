def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
    
    page = p.api.model.ui.page.getObject(params['rootobjectguid'])
    params['result'] = base64.encodestring(page.serialize(ThriftSerializer))
    
def match(q, i, p, params, tags):
	return True