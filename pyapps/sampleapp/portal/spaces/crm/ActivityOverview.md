#Activity Overview

[[sqlgrid]]
    {
        "dbconnection": "sampleapp",
        "table": "crm_view_activity_list",
        "schema": "crm_activity",
        "columns" : {
            "name": "Name",
            "description": "Description",
            "status": "Status",
            "guid": "guid"},
        "link": {"Name": "/sampleapp/#/crm/activity_detail_$guid$"},
        "sort": "name",
        "name": "Activities",
        "pagesize": 10,
        "width": 600,
        "height": 200,
        "fieldwidth": {
            "customer": 40,
            "name": 60,
            "status": 120,
            "guid":120
        },
        "hidden":["guid"]
    }
[[/sqlgrid]]

