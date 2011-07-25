__author__ = 'aserver'
__tags__ = 'events', 'raiseWarning'
__priority__= 3

def main(q, i, params, tags):
    ret = q.workflowengine.agentcontroller.executeActorActionScript(params['agentguid'], 'raise',
                                                              params, executionparams={"description":"Raise Warning"})
    if ret['result']:
        raise ret['result']

def match(q, i, params, tags):
    return True

