__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'discoverIpAddress'
from rootobjectaction_lib import rootobjectaction_find
from rootobjectaction_lib import events

def getAgentGuid():
    """
    Gets the agent guid
    """
    matches = rootobjectaction_find.racktivity_application_find(name='racktivity_agent', istemplate=None)
    if not matches:
        events.raiseError("No agent found", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0007', tags='', escalate=False)

    return matches[0]

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    
    agentguid = getAgentGuid()
    result = q.actions.actor.meteringdevice.discover(agentguid, params['ipaddress'], params['port'], params['communitystring'])
    
    params['result'] = result['result']
  

def match(q, i, params, tags):
    return True

