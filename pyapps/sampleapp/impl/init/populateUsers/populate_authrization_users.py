__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 6

from osis.store.OsisDB import OsisDB

def main(q, i, p, params, tags):
    api=p.application.getAPI("sampleapp",context=q.enumerators.AppContext.APPSERVER)

    user = api.model.crm.user.new()
    user.name = "superadmin"
    user.password = "superadmin"
    user.groups = "admins,salespersons"
    api.model.crm.user.save(user)
    
    user = api.model.crm.user.new()
    user.name = "sysadmin"
    user.password = "sysadmin"
    user.groups = "admins"
    api.model.crm.user.save(user)
    
    user = api.model.crm.user.new()
    user.name = "salesperson"
    user.password = "salesperson"
    user.groups = "salesperson"
    api.model.crm.user.save(user)
    
    
    permission = api.model.crm.permission.new()
    permission.name = "admins"
    permission.uri = "/sampleapp/#/protected/admins"
    api.model.crm.permission.save(permission)
    
    permission = api.model.crm.permission.new()
    permission.name = "sales"
    permission.uri = "/sampleapp/#/protected/sales"
    api.model.crm.permission.save(permission)
    
    group = api.model.crm.group.new()
    group.name = "admins"
    group.permissions = "/sampleapp/#/protected/admins"
    api.model.crm.group.save(group)
    
    group = api.model.crm.group.new()
    group.name = "sales"
    group.permissions = "/sampleapp/#/protected/sales"
    api.model.crm.group.save(group)
    
    
    
    
    
    
    
