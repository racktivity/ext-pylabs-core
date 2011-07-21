__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    podguid = params['podguid']
    pod = p.api.model.racktivity.pod.get(podguid)
    pod.racks.remove(params['rackguid'])
    p.api.model.racktivity.pod.save(pod)
    
    #import racktivityui.uigenerator.pod
    #racktivityui.uigenerator.pod.update(podguid)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
