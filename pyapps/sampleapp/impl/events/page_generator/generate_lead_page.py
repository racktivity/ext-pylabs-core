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
    lead = p.api.action.crm.lead.getObject(guid)['result']
    if lead.customerguid:
        customer = p.api.action.crm.customer.getObject(guid)['result']
        customername = customer.name
    else:
        customername = '<No related customer>'
    
    searchresult = p.action.ui.page.find(name="lead_detail_%s"%guid)['result']
    if searchresult:
        p.action.ui.page.update(guid, "lead_detail_%s"%guid, "crm", "lead", "crm lead", 
                                template%{"name": lead.name, "code": lead.code, "customer": customername, "source": lead.source,
                                          "type": lead.type, "status": lead.status, "amount": lead.amount, "probability": lead.probability})
    else:
        p.action.ui.page.create("lead_detail_%s"%guid, "crm", "lead", "crm lead", 
                                template%{"name": lead.name, "code": lead.code, "customer": customername, "source": lead.source,
                                          "type": lead.type, "status": lead.status, "amount": lead.amount, "probability": lead.probability})
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.lead'