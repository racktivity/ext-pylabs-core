def main(q, i, p, params, tags):
    page = p.api.model.ui.page.get(params['pageguid'])
    page.name = params['name']
    page.space = params['space']
    page.category = params['category']
    page.parent = params.get('parent')
    page.tags = params.get('tags')
    page.content = params.get('content')            
    p.api.model.ui.page.save(page)
    params['result'] = True
    
def match(q, i, p, params, tags):
	return True
