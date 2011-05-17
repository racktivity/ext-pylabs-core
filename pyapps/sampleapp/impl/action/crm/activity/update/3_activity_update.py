from datetime import datetime
__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    activity = p.api.model.crm.activity.get(params['activityguid'])
    columns = ('name', 'description', 'location','type', 'priority', 'status', 'customerguid', 'leadguid')
    for column in columns:
        value = params.get(column)
        if value is not None:
            setattr(activity, column, value)
    activity.starttime =  datetime.fromtimestamp(int(params['starttime'])) if params['starttime'] else activity.starttime
    activity.endtime = datetime.fromtimestamp(int(params['endtime'])) if params['endtime'] else activity.endtime
    p.api.model.crm.activity.save(activity)
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
