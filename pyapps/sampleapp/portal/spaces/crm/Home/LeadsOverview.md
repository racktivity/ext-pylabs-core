#Leads Overview

[[sqlgrid]]
{
    "dbconnection": "sampleapp",
    "table": "crm_view_lead_list",
    "schema": "crm_lead",
	"columns" : {
		        "name": "Name",
		        "probability" : "Probability",
		        "source": "Source",
				"amount": "Amount",
				"guid": "guid"},
    "name": "Leads",
    "link": {"Name": "/sampleapp/#/crm/lead_detail_$guid$"},
    "sort": "name",
    "pagesize": 10,
    "width": 600,
    "height": 200,
    "fieldwidth": {
        "name": 80
    },
    "hidden":["guid"]
    
}
[[/sqlgrid]]

[[wizard:title=Add,domain=crm,name=lead_create]][[/wizard]]
