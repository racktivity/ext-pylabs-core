__author__ = 'incubaid'

def main(q, i, p, params, tags):
    
    params['result'] = q.workflowengine.agentcontroller.executeActorActionScript(agentguid = 'agent1', scriptname      = 'sendMail', params = params, 
                                                                                 executionparams = {"maxduration": 30, "description": "Sending welcome mail to customer"})['result']
    
def match(q, i, p, params, tags):
	return True