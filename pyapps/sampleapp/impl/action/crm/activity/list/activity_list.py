__tags__ = 'activity','list'
__author__ = 'incubaid'

from osis.store.OsisDB import OsisDB


def main(q, i, p, params, tags):
    filterObject = p.api.model.crm.activity.getFilterObject()
    
    fields = ("name", "description", "location", "type", "priority", "status", "customerguid", "leadguid", "starttime", "endtime")
    for key,value in params.iteritems():
        if key in fields and not value in (None, ''):
            filterObject.add('crm_view_activity_list', key, value)
    
    result = p.api.model.crm.activity.findAsView(filterObject, 'crm_view_activity_list')
    params['result'] = result
    
def match(q, i, p, params, tags):
    return True