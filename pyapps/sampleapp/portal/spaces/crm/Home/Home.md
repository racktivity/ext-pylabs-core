#CRM Home

[[pagetree]][[/pagetree]]

[[sqlgrid]]
    {
        "dbconnection": "sampleapp",
        "table": "ui_view_page_list",
        "schema": "ui_page",
        "columns" : {
            "name": "Name",
            "category" : "Category",
            "space": "Space"},
        "wheredict": {
            "space" : "crm"
        },
        "link": {"Name": "/sampleapp/#/crm/$Name$"},
        "sort": "name",
        "name": "Pages",
        "pagesize": 10,
        "width": 600,
        "height": 490,
        "fieldwidth": {
            "category": 40,
            "name": 60,
            "parent": 120,
            "space": 70
        }
    }
[[/sqlgrid]]



