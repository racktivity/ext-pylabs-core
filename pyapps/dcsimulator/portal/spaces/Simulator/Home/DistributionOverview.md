#Business Params DC Distribution Overview

[[sqlgrid]]
{
    "dbconnection": "dcsimulator",
    "table": "datacenter_view_businessparams_list",
    "schema": "datacenter_businessparams",
    "columns" : {
            "name": "Name",
            "collocation": "% Collocation",
            "cpu": "%CPU Racks",
            "storage": "%Storage Racks",
            "guid": "guid"},
    "sort": "name",
    "name": "Distribution",
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

<br/>

[[wizard:title=Rack Distribution, name=rackdistribution, type=button, domain=datacenter]][[/wizard]]