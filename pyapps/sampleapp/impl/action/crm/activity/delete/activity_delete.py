__author__ = 'Incubaid'
__tags__ = 'activity', 'delete'
__priority__= 3

def main(q, i, p, params, tags):
    p.api.model.crm.activity.delete(params['rootobjectguid'])
    
def match(q, i, p, params, tags):
    return True