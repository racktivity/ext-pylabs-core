# Permission Overview


<div class="macro macro_sqlgrid">
{
    "dbconnection": "sampleapp",
    "table": "crm_view_permission_list",
    "schema": "crm_permission",
    "columns" : {
            "name": "Name",
            "uri": "Uri",
            "guid": "guid"
            },
    "link" : {
            "Name":"/sampleapp/#/crm/permission_detail_$guid$",
            "Uri":"/sampleapp/#/crm/permission_detail_$guid$",
    "": ""
    },
 
    "name": "Permissions",
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

[[wizard:title=Add, name=permission_create]][[/wizard]]
