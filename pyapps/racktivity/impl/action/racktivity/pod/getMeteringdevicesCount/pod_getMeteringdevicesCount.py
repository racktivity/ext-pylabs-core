__author__ = 'racktivity'
__priority__= 3

from rootobjectaction_lib import rootobjectaction_find, rootobjectaction_list

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    podguid = params['podguid']
    #datacenter = p.api.model.racktivity.datacenter.get()
    
    configured = 0
    used = 0
    identified = 0
    
    for rowguid in rootobjectaction_find.row_find(pod=podguid):
        row = p.api.model.racktivity.row.get(rowguid)
        for rackguid in row.racks:
            for md in rootobjectaction_list.meteringdevice_list(rackguid=rackguid):
                if md['parentmeteringdeviceguid']:
                    continue
                
                status = md['meteringdeviceconfigstatus']
                if status == 'CONFIGURED':
                    configured += 1
                elif status == 'USED':
                    used += 1
                elif status == 'IDENTIFIED':
                    identified += 1
                    
    pod = p.api.model.racktivity.pod.get(podguid)
    for rackguid in pod.racks:
        for md in rootobjectaction_list.meteringdevice_list(rackguid=rackguid):
            if md['parentmeteringdeviceguid']:
                continue
            
            status = md['meteringdeviceconfigstatus']
            if status == 'CONFIGURED':
                configured += 1
            elif status == 'USED':
                user += 1
            elif status == 'IDENTIFIED':
                identified += 1
    
    params['result'] = {'returncode': True, 'count': {'configured': configured,
                                                      'identified': identified,
                                                      'used': used,
                                                      'total': configured + identified + used}}
    
def match(q, i, params, tags):
    return True
