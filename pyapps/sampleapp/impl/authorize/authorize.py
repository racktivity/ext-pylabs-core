__tags__ = 'authorize', 
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


def getUserGroups(p, username):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % ("crm", "user")
    filter = p.api.model.crm.user.getFilterObject()
    filter.add(viewname, "name", username)
    user = osis.objectsFindAsView("crm", "user", filter, viewname)
    
    return user[0]['groups'].split(",") 
    
    
    
    
def getAllowedPermissions(p, username):
    userGroups = getUserGroups(p, username)
    if len (userGroups) == 0:
        return None 
    
    groups=""
    for group in  userGroups:
        groups += ( ",'%s'"%group.strip())
    
    groups = groups[1:]
            
    
    allowedPermissions =set()
    
    osis = p.application.getOsisConnection(p.api.appname)
    allowedPermissionPerGroup = osis.runQuery("select permissions from %s_%s.%s_view_%s_list where name in (%s)"%("crm","group","crm","group",groups))
    for permissionString in allowedPermissionPerGroup:
        permissins= permissionString['permissions'].split(",")
        allowedPermissions.update(permissins)
    
    
    permissions= [("/sampleapp/appserver/rest/ui/portal/page?space=%s&name=%s"%(permission.split("/")[-2],permission.split("/")[-1])).strip() for permission in allowedPermissions]
     
    return permissions

def main(q, i, p,params, tags):
    request = params['request']
    criteria = params['criteria']
    domain =  params['domain']
    service = params['service']
    methodname = params['methodname']
    args = params['args']
    kwargs = params['kwargs']
    
    
    if request._request.uri not in getpermissions(p) :
        params['result'] = True
        return
    
    if request._request.uri not in  getAllowedPermissions(p, request.username):
        params['result']= False
    else:
        params['result']= True
 
def match(q, i, params, tags):
    return True
