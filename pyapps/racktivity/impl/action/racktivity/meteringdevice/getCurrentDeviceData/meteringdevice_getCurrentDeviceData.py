__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    datatype = params['meteringtype'] #Can be totalpower, totalvoltage, and totalcurrent    
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)

    result = q.actions.actor.meteringdevice.getDeviceData(meteringdeviceguid, master.meteringdevicetype, master.network.ipaddress, master.network.port, meteringdevice.id, datatype, master.accounts[0].login, master.accounts[0].password)
    params['result'] = result['result']
  

def match(q, i, params, tags):
    return True

