__author__ = 'racktivity'

def main(q, i, params, tags):
    ret = q.workflowengine.agentcontroller.executeActorActionScript(params['agentguid'], 'raise',
                                                              params, executionparams={"description":"Raise Error"})
    if ret['result']:
        raise ret['result']

def match(q, i, params, tags):
    return True

