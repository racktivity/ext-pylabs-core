#Customer Overview

<div class="macro macro_sqlgrid">
{
    "dbconnection": "sampleapp",
    "table": "crm_view_customer_list",
    "schema": "crm_customer",
    "sqlselect": "SELECT crm_view_customer_list.name, crm_view_customer_list.guid FROM crm_customer.crm_view_customer_list",
    "link": {"name": "/sampleapp/#/crm/customer_detail_$guid$"},
    "sort": "name",
    "name": "Customers",
    "pagesize": 10,
    "width": 600,
    "height": 200,
    "fieldwidth": {
        "category": 40,
        "name": 80,
        "parent": 160
    },
    "hidden":["guid"]
}
</div>

[[wizard:title=Create Customer,name=customer_create]][[/wizard]]
