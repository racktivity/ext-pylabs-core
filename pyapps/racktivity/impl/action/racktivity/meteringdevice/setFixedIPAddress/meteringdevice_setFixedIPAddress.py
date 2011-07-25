__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    changed = False
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)
    #update meteringdevice
    oldipaddress = master.network.ipaddress
    master.network.ipaddress = params['ipaddress']
    p.api.model.racktivity.meteringdevice.save(master)
    q.actions.actor.meteringdevice.setConfigurationParameter(master.guid, master.meteringdevicetype, oldipaddress, master.network.port, meteringdevice.id, 'IPAddress', params['ipaddress'])
    q.actions.actor.meteringdevice.setConfigurationParameter(master.guid, master.meteringdevicetype, oldipaddress, master.network.port, meteringdevice.id, 'SubNetMask', params['subnetmask'])
    q.actions.actor.meteringdevice.setConfigurationParameter(master.guid, master.meteringdevicetype, oldipaddress, master.network.port, meteringdevice.id, 'StdGateWay', params['defaultgateway'])
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
