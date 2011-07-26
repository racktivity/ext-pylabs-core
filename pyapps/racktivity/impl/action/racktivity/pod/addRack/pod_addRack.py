__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    podguid = params['podguid']
    rackguid = params['rackguid']
    pod = p.api.model.racktivity.pod.get(podguid)
    if rackguid in pod.racks:
        raise ValueError("The rack already exists in the given pod")
    from rootobjectaction_lib import rootobjectaction_list
    if not rootobjectaction_list.rack_list(rackguid=rackguid):
        raise ValueError("Rack with guid %s is not found in the system"%rackguid)
    pod.racks.append(rackguid)
    p.api.model.racktivity.pod.save(pod)
    p.api.action.racktivity.rack.uiCreatePageUnderParent(rackguid, podguid, request = params["request"])

    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
