__tags__ = 'customer','list'
__author__ = 'incubaid'

from osis.store.OsisDB import OsisDB


def main(q, i, p, params, tags):
    filterObject = p.api.model.crm.customer.getFilterObject()
    
    fields = ("name", "login", "password", "email", "address", "vat", "status")
    for key,value in params.iteritems():
        if key in fields and not value in (None, ''):
            filterObject.add('crm_view_customer_list', key, value)
    
    result = p.api.model.crm.customer.findAsView(filterObject, 'crm_view_customer_list')
    params['result'] = result
    
def match(q, i, p, params, tags):
    return True