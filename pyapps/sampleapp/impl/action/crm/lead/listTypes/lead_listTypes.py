__tags__ = 'lead','listTypes'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    params['result'] = q.enumerators.leadtype._pm_enumeration_items
    
def match(q, i, p, params, tags):
	return True