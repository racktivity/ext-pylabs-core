import urllib
try:
    import json
except ImportError:
    import simplejson as json

def main(q, i, p, params, tags):
    guid = params["eventBody"]
    template = """# Customer details

*   **Name:** %(name)s
*   **Login:** %(login)s
*   **Password:** %(password)s
*   **Email:** %(email)s
*   **Address:** %(address)s
*   **VAT:** %(vat)s
*   **Status:** %(status)s
<br />
<br />
[[wizard:title=Edit, name=customer_edit, extra=%(params)s]][[/wizard]]
[[wizard:title=Delete, name=customer_delete, extra=%(params)s]][[/wizard]]
<br />
<div class="macro macro_sqlgrid">
    {
        "dbconnection": "sampleapp",
        "table": "crm_view_lead_list",
        "schema": "crm_lead",
        "columns": {
            "name":"Lead Name"
            },
        "wheredict": {
            "customerguid":"%(customerguid)s"
            },
        "sort": "name",
        "pagesize": 10,
        "width": 300,
        "height": 300,
        "fieldwidth": {
            "name": 120,
            "source": 120,
            "type": 120,
            "status": 120
        }
    }

</div>
<br />
[[wizard:title=Create New Lead, name=lead_create, extra=%(params)s]][[/wizard]]
"""
    customer = p.api.action.crm.customer.getObject(guid)
    searchresult = p.api.action.ui.page.find(name="customer_detail_%s"%guid)['result']
    parentpage = p.api.action.ui.page.find(name="Home", space="crm")['result'][0]

    params_ = urllib.quote(json.dumps({'customerguid': customer.guid}))
    
    if searchresult:
        p.api.action.ui.page.update(
            searchresult[0],
            "customer_detail_%s" % guid,
            "crm",
            "customer",
            parentpage,
            "crm customer",
            template % {"name": customer.name, "login": customer.login, "password": customer.password, "email": customer.email,
                                          "address": customer.address, "vat": customer.vat, "status": customer.status,
                                          "customerguid" : customer.guid,
                                          'params': params_, })
    else:
        p.api.action.ui.page.create(
            "customer_detail_%s" % guid,
            "crm",
            "customer",
            parentpage,
            "crm customer",
            template % {"name": customer.name, "login": customer.login, "password": customer.password, "email": customer.email,
                                          "address": customer.address, "vat": customer.vat, "status": customer.status,
                                          "customerguid" : customer.guid,
                                          'params': params_, })
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.customer'
