__tags__ = "test", "setup"
__author__ = "racktivity"
__priority__ = 80

def main(q, i, params, tags):
    q.qp._runPendingReconfigeFiles()
    
    #Patch the agent
    from time import sleep
    ca = i.config.cloudApiConnection.find("main")
    agentGuid = ca.racktivity_application.find(name = 'racktivity_agent')['result']['guidlist'][0]
    wfeGuid = q.config.getConfig("Workflowengine")['main']["agentcontrollerguid"]
    usrs  = (q.manage.ejabberd.cmdb.users[agentGuid], q.manage.ejabberd.cmdb.users[wfeGuid])
    q.manage.applicationserver.stop()
    q.manage.workflowengine.stop()
    
    q.manage.ejabberd.startChanges()
    for usr in usrs:
        q.manage.ejabberd.cmdb.removeUser(usr.name)
        try:
            del q.manage.ejabberd.cmdb.users[usr.name]
        except:
            pass
    q.manage.ejabberd.cmdb.save()
    q.manage.ejabberd.applyConfig()
    
    q.manage.ejabberd.stop()
    q.system.fs.removeDirTree("/opt/qbase3/apps/ejabberd/var/lib/ejabberd/db/")
    for x in range(0,5):
        q.manage.ejabberd.start()
        sleep(1)
    
    q.manage.ejabberd.startChanges()
    for usr in usrs:
        q.manage.ejabberd.cmdb.addUser(usr.name , usr.server, usr.password)
    q.manage.ejabberd.cmdb.save()
    q.manage.ejabberd.applyConfig()
    
    q.manage.workflowengine.start()
    sleep(5)
    q.manage.applicationserver.start()

def match(q, i, params, tags):
    return params['stage'] == 2