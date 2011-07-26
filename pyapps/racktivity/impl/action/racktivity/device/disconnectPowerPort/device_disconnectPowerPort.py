__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    portname = params.get('portname')
    cableguid = params.get('cableguid')
    q.logger.log('Disconnect powerport %s' % portname, 3)
    device = p.api.model.racktivity.device.get(params['deviceguid'])
    for port in device.powerports:
        if (portname and port.name == portname) or (cableguid and port.cableguid == cableguid):
            cableguid = port.cableguid
            port.cableguid = None
            port.status = q.enumerators.powerportstatustype.NOTCONNECTED
            p.api.model.racktivity.device.save(device) 
            from rootobjectaction_lib import rootobjectaction_find
            meteringdeviceguids = rootobjectaction_find.find("meteringdevice", cableguid=cableguid)
            for meteringdeviceguid in meteringdeviceguids:
                p.api.action.racktivity.meteringdevice.disconnectPowerOutputPort(meteringdeviceguid, cableguid=cableguid, request = params["request"])
            #check if the cable still exists
            from rootobjectaction_lib import rootobjectaction_list
            if rootobjectaction_list.cable_list(cableguid):
                p.api.action.racktivity.cable.delete(cableguid, request = params["request"])
            break
    params['result'] = {'returncode': True, 'deviceguid': device.guid}

def match(q, i, params, tags):
    return True

