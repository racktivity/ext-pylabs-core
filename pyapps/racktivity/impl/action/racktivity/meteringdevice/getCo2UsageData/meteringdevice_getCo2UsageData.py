__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getCo2UsageData'

from rootobjectaction_lib import rootobjectaction_find
from rootobjectaction_lib import events

CO2_MAP = {'COAL': 1150,
           'GENERIC': 0,
           'NUCLEAR': 6,
           'GAS': 430,
           'GENERIC_GREEN':0,
           'WIND': 12,
           'SOLAR': 105}

def getFeed(powerinputs):
    feedguids = set()
    
    for input in powerinputs:
        feedguids = feedguids.union(rootobjectaction_find.feed_find(cableguid=input.cableguid))
    
    if len(feedguids) > 1:
        events.raiseError("Metering device has multiple feeds (sources)", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0048', tags='', escalate=False)
    elif len(feedguids) == 0:
        events.raiseError("Metering device is not connected to any feed", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0049', tags='', escalate=False)

    return feedguids.pop()

def main(q, i, params, tags):
    params['result'] = {'returncode': False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    
    powerinputs = list()
    for input in meteringdevice.powerinputs:
        if input.cableguid:
            powerinputs.append(input)
    
    feedguid = getFeed(powerinputs)
    feed = q.drp.feed.get(feedguid)
    
    devicedata = q.actions.rootobject.meteringdevice.getCurrentDeviceData(meteringdeviceguid, "all", request = params["request"])['result']['value']
    
    co2emission = CO2_MAP[str(feed.productiontype)]
    portsdata = devicedata['Ports']
    
    portsco2 = dict()
    
    for output in meteringdevice.poweroutputs:
        index = output.sequence - 1
        portenergy = portsdata[index]['ApparentEnergy']
        portco2 = portenergy * co2emission
        portsco2[str(output.sequence)] = portco2
        
    params['result'] = {'returncode': True,
                        'value': {'meteringdevice': sum(portsco2.values()),
                                  'Ports': portsco2}
                        }
  

def match(q, i, params, tags):
    return True

