__author__ = 'racktivity'
__tags__ = 'pod', 'removeRack'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    podguid = params['podguid']
    pod = q.drp.pod.get(podguid)
    pod.racks.remove(params['rackguid'])
    q.drp.pod.save(pod)
    
    import racktivityui.uigenerator.pod
    racktivityui.uigenerator.pod.update(podguid)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
