def main(q, i, p, params, tags):
    filterObject = p.api.model.ui.page.getFilterObject()

    fields = ('name','space', 'category', 'parent', 'tags')
    for key,value in params.iteritems():
        if key in fields and not value in (None, ''):
            filterObject.add('ui_view_page_list', key, value)
          
    result = p.api.model.ui.page.find(filterObject)
    params['result'] = result

    
def match(q, i, p, params, tags):
	return True
