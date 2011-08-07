# User Overview


<div class="macro macro_sqlgrid">
{
    "dbconnection": "sampleapp",
    "table": "crm_view_user_list",
    "schema": "crm_user",
    "columns" : {
            "password": "Password",
            "name": "Name",
            "groups": "Groups",
            "guid": "guid"
            },
    "link" : {
            "Password":"/sampleapp/#/crm/user_detail_$guid$",
            "Name":"/sampleapp/#/crm/user_detail_$guid$",
            "Groups":"/sampleapp/#/crm/user_detail_$guid$",
    "": ""
    },
 
    "name": "Users",
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

[[wizard:title=Add,domain=drm,name=user_create]][[/wizard]]
