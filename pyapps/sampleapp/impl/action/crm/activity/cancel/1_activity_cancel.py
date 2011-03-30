__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    activity = p.api.action.crm.activity.getObject(params['rootobjectguid'])
    activity.status = q.enumerators.activitystatus.CANCELLED
    activity.save()
    
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True