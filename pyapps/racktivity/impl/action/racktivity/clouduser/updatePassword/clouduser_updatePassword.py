__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params, nameKey = "login")
    params['result'] = {'returncode':False}

    clouduserguid = params['clouduserguid'] 
    currentpassword = params['currentpassword']
    newPassword = params['newpassword']
    
    clouduser = p.api.model.racktivity.clouduser.get(clouduserguid)
     
    def updateModel():
        if clouduser.password == currentpassword:
            clouduser.password = newPassword
            p.api.model.racktivity.clouduser.save(clouduser)
        else:
            q.eventhandler.raiseError('Invalid current password')
   
    if clouduser.login == 'admin' or clouduser.login == 'monitoring':
        cloudAPI = i.config.cloudApiConnection.find('main')
        applianceAgentGuid = cloudAPI.machine.getApplianceAgent()['result']
        applianceGuid = cloudAPI.machine.find(agentguid=applianceAgentGuid)['result']
        if not applianceGuid:
            q.eventhandler.raiseError('No appliance machine found, cannot continue')
        applianceGuid = applianceGuid[0]
        
        
        pmachines = cloudAPI.machine.find(machinetype='PHYSICAL', osguid='3f8bee68-c7ed-4a45-b222-57b1931443f4')['result']
        pmachines.remove(applianceGuid)

        if clouduser.login <> 'admin':
            updateModel()     
        #First change config of non appliance nodes
        for pmachine in pmachines:
            p.api.actor.pmachine.reconfigureUser(machineguid = pmachine,
                                                     clouduserguid =  clouduser.guid,
                                                     newpassword =  newPassword,
                                                     executionparams={"description":"Reconfigure user on machine %s" %pmachine})
            
        p.api.actor.pmachine.reconfigureUser(machineguid = applianceGuid,
                                                 clouduserguid =  clouduser.guid,
                                                 newpassword =  newPassword,
                                                 executionparams={"description":"Reconfigure user on machine %s" %applianceGuid})        
    if clouduser.login == 'admin':
        p.api.actor.systemnas.setCredentials(clouduser.login, newPassword)
    updateModel()

    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
