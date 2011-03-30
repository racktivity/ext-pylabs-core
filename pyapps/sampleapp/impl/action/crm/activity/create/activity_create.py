__author__ = 'Incubaid'
__priority__= 3

def main(q, i, p, params, tags):
    activity = p.api.model.crm.activity.new()
    activity.name = params['name']
    activity.description = params['description']
    activity.location = params['location']
    activity.type = params['type']
    activity.priority = params['priority']
    activity.status = params['status']
    activity.customerguid = params['customerguid']
    activity.leadguid = params['leadguid']
    activity.starttime = params['starttime']
    activity.endtime = params['endtime']
    activity.save()
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True