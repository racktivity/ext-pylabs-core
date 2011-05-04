from datetime import datetime
__author__ = 'Incubaid'
__priority__= 3

def main(q, i, p, params, tags):
    q.logger.log("[activity_create_action]Creating activity for lead "+params['leadguid'],level=10)
   
    activity = p.api.model.crm.activity.new()
    activity.name = params['name']
    activity.description = params['description']
    activity.location = params['location']
    activity.type =  params['type']
    activity.priority = params['priority']
    activity.status = params['status'] 
    activity.customerguid = params['customerguid']
    activity.leadguid = params['leadguid']
    activity.starttime =  datetime.fromtimestamp(int(params['starttime']))
    activity.endtime = datetime.fromtimestamp(int(params['endtime'])) 
    p.api.model.crm.activity.save(activity)
    #activity.save()
    params['result'] = activity.guid
    
def match(q, i, p, params, tags):
    return True