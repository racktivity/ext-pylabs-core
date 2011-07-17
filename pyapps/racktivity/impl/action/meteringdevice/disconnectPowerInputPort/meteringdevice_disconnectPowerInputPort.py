__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'disconnectPowerInputPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    portlabel = params.get('portlabel')
    cableguid = params.get('cableguid')
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    input = None
    for powerinput in meteringdevice.powerinputs:
        if (portlabel and powerinput.label == portlabel) or (cableguid and powerinput.cableguid == cableguid):
            input = powerinput
            break
    
    if not input:
        events.raiseError("No port found", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0031', tags='', escalate=False)

    cableguid = input.cableguid
    input.cableguid = None
    q.drp.meteringdevice.save(meteringdevice)
    
    from rootobjectaction_lib import rootobjectaction_find
    for deviceguid in rootobjectaction_find.device_find(cableguid=cableguid):
        q.actions.rootobject.device.disconnectPowerPort(deviceguid, cableguid=cableguid, request = params["request"])
    #check if the cable still exists
    from rootobjectaction_lib import rootobjectaction_list
    if rootobjectaction_list.cable_list(cableguid):
        q.actions.rootobject.cable.delete(cableguid, request = params["request"])
            
    params['result'] = {'returncode':True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True