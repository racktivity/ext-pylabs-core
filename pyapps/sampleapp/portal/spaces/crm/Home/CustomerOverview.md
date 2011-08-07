#Customer Overview

[[sqlgrid]]
{
    "dbconnection": "sampleapp",
    "table": "crm_view_customer_list",
    "schema": "crm_customer",
    "columns" : {
            "name": "Name",
            "guid": "guid"},
    "link": {"Name": "/sampleapp/#/crm/customer_detail_$guid$"},
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
[[/sqlgrid]]
[[wizard:title=Create Customer,domain=crm,name=customer_create]][[/wizard]]
