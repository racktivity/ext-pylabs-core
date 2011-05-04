def main(q, i, p, params, tags):
    eventKey_list = params["eventKey"].split('.')
    
    page_name = "%s_detail_%s"%(eventKey_list[-1], params["eventBody"])
    
    page_space = "crm"
    
    page_guid_list = p.api.action.ui.page.find(page_name, page_space)['result']
    
    for page_guid in page_guid_list:
        p.api.action.ui.page.delete(page_guid)
    
def match(q, i, params, tags):
    return 'pylabs.event.sampleapp.osis.delete.crm.' in params["eventKey"]
