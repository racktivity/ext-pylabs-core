import json

def main(q, i, p, params, tags):
    guid = params["eventBody"]
    key = params["eventKey"]
    template = """
# User details
* __Password:__ %(password)s
* __Name:__ %(name)s
* __Groups:__ %(groups)s
[[wizard:title=Edit, name=user_edit, extra=%(wizard_params)s]][[/wizard]]
[[wizard:title=Delete, name=user_delete, extra=%(wizard_params)s]][[/wizard]]

    """
    try:
        user = p.api.action.crm.user.getObject(guid)
    except:
        raise Exception("Error getting user with guid %s"% guid )
    
    
    wizard_params = json.dumps({'userguid': user.guid})
    q.logger.log("search view for user %s"%guid,level=3) 
    searchresult = p.api.action.ui.page.find(name="user_detail_%s"%guid)['result']
    q.logger.log("search returned view %s"%str(searchresult),level=3)
    parentpage = p.api.action.ui.page.find(name="UserOverview", space="crm")['result'][0]
    
    templateParams= dict()
    templateParams['wizard_params'] = wizard_params
    templateParams['userguid'] = guid
    templateParams['password']=user.password
    templateParams['name']=user.name
    templateParams['groups']=user.groups
    
    content = template% templateParams 
    
    if searchresult:
        p.api.action.ui.page.update(searchresult[0], "user_detail_%s"%guid, "crm", "user", parentpage, "crm user",content)
    else:
        p.api.action.ui.page.create("user_detail_%s"%guid, "crm", "user", parentpage, "crm user",content)        
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.user'
