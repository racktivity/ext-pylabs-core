__tags__ = 'authenticate', 
__author__ = 'Incubaid'

def getpermissions(p):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % ("crm", "permission")
    permissionsList = osis.objectsFindAsView("crm",
        "permission",
        p.api.model.crm.permission.getFilterObject(),
        viewname)

    permissions= ["/sampleapp/appserver/rest/ui/portal/page?space=%s&name=%s"%(permission['uri'].split("/")[-2],permission['uri'].split("/")[-1]) for permission in permissionsList]
    return permissions

def isUserCeridentialsVaild(p,username, password):
    osis = p.application.getOsisConnection(p.api.appname)
    filter = p.api.model.crm.permission.getFilterObject()
    viewname = '%s_view_%s_list' % ("crm", "user")
    filter.add(viewname, "name", username)
    filter.add(viewname, "password", password)
    
    user = osis.objectsFindAsView("crm","user",filter, viewname)
    
    if user: 
        return True
    else:
        return False
    
    
def main(q, i, p, params, tags):
    request = params['request']
        


 
    permissions = getpermissions(p) 
        
    if request._request.uri.endswith("logout"):
        params['result'] = False
        return
   
    if request._request.uri not in permissions :
        params['result'] = True
        return
        
    else:
        
     
        if not request.username or not request.password:
            params['result'] = False
            return
         
   
        if isUserCeridentialsVaild(p,request.username, request.password): 
            #request.username
            params['result'] = True
        else:
            params['result'] = False
            return
        
    
    result =params.get('result', False)

  
            
def match(q, i, params, tags):
    return True
