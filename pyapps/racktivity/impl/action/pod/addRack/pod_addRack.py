__author__ = 'racktivity'
__tags__ = 'pod', 'addRack'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    podguid = params['podguid']
    rackguid = params['rackguid']
    pod = q.drp.pod.get(podguid)
    if rackguid in pod.racks:
        raise ValueError("The rack already exists in the given pod")
    from rootobjectaction_lib import rootobjectaction_list
    if not rootobjectaction_list.rack_list(rackguid=rackguid):
        raise ValueError("Rack with guid %s is not found in the system"%rackguid)
    pod.racks.append(rackguid)
    q.drp.pod.save(pod)
    q.actions.rootobject.rack.uiCreatePageUnderParent(rackguid, podguid, request = params["request"])
    import racktivityui.uigenerator.pod
    racktivityui.uigenerator.pod.update(podguid)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
