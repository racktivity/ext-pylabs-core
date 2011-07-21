__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    from rootobjectaction_lib import rootobject_tree
    mdguids = rootobject_tree.getMeteringDevices(params["guid"], tags[0])
    from rootobjectaction_lib import rootobject_authorization
    mdguids = rootobject_authorization.getAuthorizedGuids(params["request"]["username"], mdguids, p.api.model.racktivity.meteringdevice, "getHealtStatus")
    result = [0,0,0]
    for mdguid in mdguids:
        mdresult = p.api.action.racktivity.meteringdevice.getPduHealthStatus(mdguid, params["timing"])["result"]["healthstatus"]
        result = [a+b for a,b in zip(mdresult,result)]
    params['result'] = {"returncode":0, "healthstatus":result}

def match(q, i, params, tags):
    return True