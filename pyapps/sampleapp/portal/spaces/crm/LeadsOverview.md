#Leads Overview

<div class="macro macro_sqlgrid">
{
    "dbconnection": "sampleapp",
    "table": "crm_view_lead_list",
    "schema": "crm_lead",
    "sqlselect": "SELECT   crm_view_lead_list.name, crm_view_lead_list.probability, crm_view_lead_list.source, crm_view_lead_list.guid, crm_view_lead_list.amount FROM crm_lead.crm_view_lead_list",
    "name": "Leads",
    "link": {"name": "/sampleapp/#/crm/lead_detail_$guid$"},
    "sort": "name",
    "pagesize": 10,
    "width": 600,
    "height": 200,
    "fieldwidth": {
        "name": 80
    },
    "hidden":["guid"]
    
}
</div>

[[wizard:title=Add, name=lead_create]][[/wizard]]
