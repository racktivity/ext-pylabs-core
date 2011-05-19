try:
    import json
except ImportError:
    import simplejson as json
def main(q, i, p, params, tags):
    guid = params["eventBody"]
    key = params["eventKey"]
    template = """
# Lead details

* __Name:__ %(name)s
* __Code:__ %(code)s
* __Customer:__ %(customer)s
* __Source:__ %(source)s
* __Type:__%(type)s        
* __Status:__ %(status)s
* __Amount:__ %(amount)s 
* __Probability:__ %(probability)s

[[wizard:title=Add Activity, name=activity_create , extra=%(params)s ]][[/wizard]]
[[wizard:title=Edit, name=lead_edit , extra=%(params)s ]][[/wizard]]
<br />
[[sqlgrid]]
   {
        "dbconnection": "sampleapp",
        "table": "crm_view_activity_list",
        "schema": "crm_activity",
        "columns": {
            "name":"Name",
            "location":"Location",
            "guid": "guid"
            },
        "wheredict": {
            "lead":"%(leadguid)s"
            },
        "link": {"Name": "/sampleapp/#/crm/activity_detail_$guid$"},
        "sort": "name",
        "name": "Activities",
        "pagesize": 10,
        "width": 300,
        "height": 300,
        "hidden":["guid"]
    }
[[/sqlgrid]]
<br />       
    """
    lead = p.api.action.crm.lead.getObject(guid)
    if lead.customerguid:
        customer = p.api.action.crm.customer.getObject(lead.customerguid)
        customername = customer.name
    else:
        customername = '<No related customer>'
    
    params = json.dumps({'leadguid': lead.guid})
    q.logger.log("search view for lead %s"%guid,level=3) 
    searchresult = p.api.action.ui.page.find(name="lead_detail_%s"%guid)['result']
    q.logger.log("search returned view %s"%str(searchresult),level=3)
    parentpage = p.api.action.ui.page.find(name="Leads_Overview", space="crm")['result'][0]
    
    if searchresult:
        p.api.action.ui.page.update(searchresult[0], "lead_detail_%s"%guid, "crm", "lead", parentpage, "crm lead", 
                                template%{"params":params,"leadguid":guid,"name": lead.name, "code": lead.code, "customer": customername, "source": lead.source,
                                          "type": lead.type, "status": lead.status, "amount": lead.amount, "probability": lead.probability})
    else:
        p.api.action.ui.page.create("lead_detail_%s"%guid, "crm", "lead", parentpage, "crm lead", 
                                template%{"params":params,"leadguid":guid,"name": lead.name, "code": lead.code, "customer": customername, "source": lead.source,
                                          "type": lead.type, "status": lead.status, "amount": lead.amount, "probability": lead.probability})
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.lead'
