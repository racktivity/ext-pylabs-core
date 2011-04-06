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

<div class="macro macro_actions"></div>

<form method="post" action="#/action/customer_edit">
    <button type="submit" title="Edit customer"></button>
</form>"""
    customer = p.api.action.crm.customer.getObject(guid)
    searchresult = p.api.action.ui.page.find(name="customer_detail_%s"%guid)['result']
    if searchresult:
        p.api.action.ui.page.update(
            guid,
            "customer_detail_%s" % guid,
            "crm",
            "customer",
            None,
            "crm customer",
            template % {"name": customer.name, "login": customer.login, "password": customer.password, "email": customer.email,
                                          "address": customer.address, "vat": customer.vat, "status": customer.status})
    else:
        p.api.action.ui.page.create(
            "customer_detail_%s" % guid,
            "crm",
            "customer",
            None,
            "crm customer",
            template % {"name": customer.name, "login": customer.login, "password": customer.password, "email": customer.email,
                                          "address": customer.address, "vat": customer.vat, "status": customer.status})
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.customer'
