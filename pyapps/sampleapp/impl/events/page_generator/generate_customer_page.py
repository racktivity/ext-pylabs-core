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

<div class="macro macro_sqlgrid">
    {
        "dbconnection": "sampleapp",
        "table": "crm_view_lead_list",
        "schema": "crm",
        "fields": ["name", "source", "type", "status"],
        "sort": "name",
        "pagesize": 10,
        "width": 600,
        "height": 490,
        "fieldwidth": {
            "name": 120,
            "source": 120,
            "type": 120,
            "status": 120
        }
    }

</div>

<div class="macro macro_wizardactions"></div>

<button onclick="start('sampleapp', 'crm', 'customer_edit', '%(portalip)s', '%(params)s', success)">Edit</button>
<button onclick="start('sampleapp' ,'crm' ,'customer_delete','%(portalip)s', '%(params)s', success)">Delete</button>
"""
    customer = p.api.action.crm.customer.getObject(guid)
    searchresult = p.api.action.ui.page.find(name="customer_detail_%s"%guid)['result']
    parentpage = p.api.action.ui.page.find(name="Home", space="crm")['result'][0]
    portalip = q.system.net.getIpAddress(q.system.net.getNics(up=True)[1])[0][0]

    params_ = urllib.quote(json.dumps({'customerguid': customer.guid}))
    
    if searchresult:
        p.api.action.ui.page.update(
            guid,
            "customer_detail_%s" % guid,
            "crm",
            "customer",
            parentpage,
            "crm customer",
            template % {"name": customer.name, "login": customer.login, "password": customer.password, "email": customer.email,
                                          "address": customer.address, "vat": customer.vat, "status": customer.status,
                                          "portalip": portalip, "customerguid" : customer.guid,
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
                                          "portalip": portalip, "customerguid" : customer.guid,
                                          'params': params_, })
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.customer'
