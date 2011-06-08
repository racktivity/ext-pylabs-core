__author__ = 'incubaid'

def main(q, i, p, params, tags):
    params['result'] = p.api.model.enumerators.leadsource._pm_enumeration_items.keys()
    
def match(q, i, p, params, tags):
	return True
