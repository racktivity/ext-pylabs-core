__tags__ = 'page','delete'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    p.api.model.ui.page.delete(params['pageguid'])
    params['result'] = True
    
def match(q, i, p, params, tags):
	return True