import json

def main(q, i, p, params, tags):
    guid = params["eventBody"]
    key = params["eventKey"]
    template = """
# Permission details
* __Name:__ %(name)s
* __Uri:__ %(uri)s
[[wizard:title=Edit, name=permission_edit, extra=%(wizard_params)s]][[/wizard]]
[[wizard:title=Delete, name=permission_delete, extra=%(wizard_params)s]][[/wizard]]

    """
    try:
        permission = p.api.action.crm.permission.getObject(guid)
    except:
        raise Exception("Error getting permission with guid %s"% guid )
    
    
    wizard_params = json.dumps({'permissionguid': permission.guid})
    q.logger.log("search view for permission %s"%guid,level=3) 
    searchresult = p.api.action.ui.page.find(name="permission_detail_%s"%guid)['result']
    q.logger.log("search returned view %s"%str(searchresult),level=3)
    parentpage = p.api.action.ui.page.find(name="PermissionOverview", space="crm")['result'][0]
    
    templateParams= dict()
    templateParams['wizard_params'] = wizard_params
    templateParams['permissionguid'] = guid
    templateParams['name']=permission.name
    templateParams['uri']=permission.uri
    
    content = template% templateParams 
    
    if searchresult:
        p.api.action.ui.page.update(searchresult[0], "permission_detail_%s"%guid, "crm", "permission", parentpage, "crm permission",content)
    else:
        p.api.action.ui.page.create("permission_detail_%s"%guid, "crm", "permission", parentpage, "crm permission",content)        
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.permission'
