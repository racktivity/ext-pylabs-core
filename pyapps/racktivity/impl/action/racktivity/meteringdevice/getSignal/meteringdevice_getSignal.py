__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
        
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)

    portid = None
    for port in meteringdevice.ports:
        if port.label == params['label']:
            portid = port.sequence
            break
        
    datatype = params['meteringtype'] #can be either signal_current or signal_voltage
    
    result = p.api.actor.meteringdevice.getPortData(meteringdeviceguid, master.meteringdevicetype, master.network.ipaddress, master.network.port,  meteringdevice.id, portid, datatype)
              
    params['result'] = result['value'] 
    
  

def match(q, i, params, tags):
    return True

