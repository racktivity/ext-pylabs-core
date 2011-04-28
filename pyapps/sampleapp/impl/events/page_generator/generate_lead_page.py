def main(q, i, p, params, tags):
    guid = params["eventBody"]
    key = params["eventKey"]
    template = """
    # Lead details
    *Name:* %(name)s
    *Code:* %(code)s
    *Customer:* %(customer)s
    *Source:* %(source)s
    *Type:* %(type)s        
    *Status:* %(status)s
    *Amount:* %(amount)s
    *Probability:* %(probability)s            
    """
    lead = p.api.action.crm.lead.getObject(guid)
    if lead.customerguid:
        customer = p.api.action.crm.customer.getObject(guid)
        customername = customer.name
    else:
        customername = '<No related customer>'
    
    searchresult = p.api.action.ui.page.find(name="lead_detail_%s"%guid)['result']
    parentpage = p.api.action.ui.page.find(name="Home", space="crm")['result'][0]
    
    if searchresult:
        p.api.action.ui.page.update(guid, "lead_detail_%s"%guid, "crm", "lead", parentpage, "crm lead", 
                                template%{"name": lead.name, "code": lead.code, "customer": customername, "source": lead.source,
                                          "type": lead.type, "status": lead.status, "amount": lead.amount, "probability": lead.probability})
    else:
        p.api.action.ui.page.create("lead_detail_%s"%guid, "crm", "lead", parentpage, "crm lead", 
                                template%{"name": lead.name, "code": lead.code, "customer": customername, "source": lead.source,
                                          "type": lead.type, "status": lead.status, "amount": lead.amount, "probability": lead.probability})
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.lead'
