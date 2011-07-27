__author__ = 'racktivity'


def main(q, i, params, tags):
    
    ret = q.workflowengine.agentcontroller.executeActorActionScript(params['agentguid'], 'writeFile',
                                                              params, executionparams={"description":"Write file '%s' to disk" % params['filename']})
    params['result'] = ret['result']

def match(q, i, params, tags):
    return True