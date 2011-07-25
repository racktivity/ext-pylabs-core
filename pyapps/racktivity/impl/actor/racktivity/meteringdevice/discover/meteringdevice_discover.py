__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'discover'
__priority__= 3

RSCRIPT = "meteringdevice_discover"

def main(q, i, params, tags):
    ret = q.workflowengine.agentcontroller.executeActorActionScript(params['agentguid'], RSCRIPT,
                                                              params, executionparams={"description": "Trying to disvoer IP address '%s'" % params['ipaddress']})
    
    device = ret['result']
    
    params['result'] = {'returncode': bool(device),
                        'device': device}

def match(q, i, params, tags):
    return True

