__author__ = 'racktivity'
__tags__ = 'floor', 'getMeteringdevicesCount'
__priority__= 3

from rootobjectaction_lib import rootobjectaction_find, rootobjectaction_list

def main(q, i, params, tags):
    params['result'] = {'returncode': False}
    floorguid = params['floorguid']
    #datacenter = q.drp.datacenter.get()
    
    configured = 0
    used = 0
    identified = 0
    
    for roomguid in rootobjectaction_find.room_find(floor=floorguid):
        for rackguid in rootobjectaction_find.rack_find(roomguid=roomguid):
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
                
    params['result'] = {'returncode': True, 'count': {'configured': configured,
                                                      'identified': identified,
                                                      'used': used,
                                                      'total': configured + identified + used}}
    
def match(q, i, params, tags):
    return True
