__author__ = 'incubaid'
__priority__ = 3

def main(q, i, p, params, tags):
    filterObject = p.api.model.crm.customer.getFilterObject()
    for key in params.iterkeys():
        if key == "customerguid" and params["customerguid"]:
            filterObject.add("crm_view_customer_list", "customerguid", params["customerguid"])
        if key == "name" and params["name"]:
            filterObject.add("crm_view_customer_list", "name", params["name"])
        if key == "login" and params["login"]:
            filterObject.add("crm_view_customer_list", "login", params["login"])
        if key == "email" and params["email"]:
            filterObject.add("crm_view_email_list", "email", params["email"])
        if key == "address" and params["address"]:
            filterObject.add("crm_view_customer_list", "address", params["address"])
        if key == "vat" and params["vat"]:
            filterObject.add("crm_view_customer_list", "vat", params["vat"])
        
    result = p.api.model.crm.customer.find(filterObject)
    params["result"] = result