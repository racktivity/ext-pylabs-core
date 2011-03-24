__tags__ = 'lead','listSources'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    params['result'] = q.enumerators.leadsource._pm_enumeration_items
    
def match(q, i, p, params, tags):
	return True