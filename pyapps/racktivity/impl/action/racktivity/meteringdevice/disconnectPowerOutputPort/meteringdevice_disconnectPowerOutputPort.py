__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    portlabel = params.get('portlabel')
    cableguid = params.get('cableguid')
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    output = None
    for poweroutput in meteringdevice.poweroutputs:
        if (portlabel and poweroutput.label == portlabel) or (cableguid and poweroutput.cableguid == cableguid):
            output = poweroutput
            break
    
    if not output:
        events.raiseError("No port found", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0025', tags='', escalate=False)

    cableguid = output.cableguid
    output.cableguid = None
    p.api.model.racktivity.meteringdevice.save(meteringdevice)
    
    from rootobjectaction_lib import rootobjectaction_find
    for deviceguid in rootobjectaction_find.device_find(cableguid=cableguid):
        p.api.action.racktivity.device.disconnectPowerPort(deviceguid, cableguid=cableguid, request = params["request"])
    #check if the cable still exists
    from rootobjectaction_lib import rootobjectaction_list
    if rootobjectaction_list.cable_list(cableguid):
        p.api.action.racktivity.cable.delete(cableguid, request = params["request"])

    params['result'] = {'returncode':True}
    
    #import racktivityui.uigenerator.meteringdevice
    #racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True