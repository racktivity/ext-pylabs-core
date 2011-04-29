#CRM Leads


[[wizard:title=Add, name=lead_create]][[/wizard]]

<div class="macro macro_sqlgrid">
{
    "dbconnection": "sampleapp",
    "table": "crm_view_lead_list",
    "schema": "crm_lead",
    "sqlselect": "SELECT   guid,customerguid, name, probability, viewguid, source, amount FROM crm_lead.crm_view_lead_list",
    "columns": {
        "name": "Macro name"
    },
    "name", "Leads",
    "link": "name,guid",
    "sort": "name",
    "pagesize": 10,
    "width": 600,
    "height": 200,
    "fieldwidth": {
        "name": 80
    }
    
}

</div>

