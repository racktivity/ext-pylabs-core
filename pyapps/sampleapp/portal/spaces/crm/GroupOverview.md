# Group Overview


<div class="macro macro_sqlgrid">
{
    "dbconnection": "sampleapp",
    "table": "crm_view_group_list",
    "schema": "crm_group",
    "columns" : {
            "name": "Name",
            "permissions": "Permissions",
            "guid": "guid"
            },
    "link" : {
            "Name":"/sampleapp/#/crm/group_detail_$guid$",
            "Permissions":"/sampleapp/#/crm/group_detail_$guid$",
    "": ""
    },
 
    "name": "Groups",
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

[[wizard:title=Add,domain=crm,name=group_create]][[/wizard]]
