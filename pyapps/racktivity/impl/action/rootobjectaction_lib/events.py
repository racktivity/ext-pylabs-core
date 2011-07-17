from pymonkey import q
import rootobjectaction_find

GENERIC_OBJECT_NOT_FOUND = "RACTKVITIY-MON-GENERIC-0119"
GENERIC_NO_AGENT_INSTALLED = "RACTKVITIY-MON-GENERIC-0007"


_agentguid = None
def _getAgentGuid():
    global _agentguid
    if not _agentguid:
        applicationguids = rootobjectaction_find.racktivity_application_find(name='racktivity_agent')
        if applicationguids:
            _agentguid = applicationguids[0]
        else:
            raise RuntimeError("No Agent installed on this environment")
    
    return _agentguid

def raiseCritical(message, messageprivate='', typeid='', tags='', escalate=False):
    q.actions.actor.events.raiseCritical(_getAgentGuid(),
                                         message=message,
                                         messageprivate=messageprivate,
                                         typeid=typeid,
                                         tags=tags,
                                         escalate=escalate)

def raiseError(message, messageprivate='', typeid='', tags='', escalate=False):
    q.actions.actor.events.raiseError(_getAgentGuid(),
                                         message=message,
                                         messageprivate=messageprivate,
                                         typeid=typeid,
                                         tags=tags,
                                         escalate=escalate)

def raiseUrgent(message, messageprivate='', typeid='', tags='', escalate=False):
    q.actions.actor.events.raiseUrgent(_getAgentGuid(),
                                         message=message,
                                         messageprivate=messageprivate,
                                         typeid=typeid,
                                         tags=tags,
                                         escalate=escalate)
    
def raiseInfo(message, messageprivate='', typeid='', tags='', escalate=False):
    q.actions.actor.events.raiseInfo(_getAgentGuid(),
                                         message=message,
                                         messageprivate=messageprivate,
                                         typeid=typeid,
                                         tags=tags,
                                         escalate=escalate)
    
def raiseWarning(message, messageprivate='', typeid='', tags='', escalate=False):
    q.actions.actor.events.raiseCritical(_getAgentGuid(),
                                         message=message,
                                         messageprivate=messageprivate,
                                         typeid=typeid,
                                         tags=tags,
                                         escalate=escalate)
    