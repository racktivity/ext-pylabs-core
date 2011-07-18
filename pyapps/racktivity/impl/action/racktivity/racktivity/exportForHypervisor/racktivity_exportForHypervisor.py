__author__ = 'racktivity'
__tags__ = 'racktivity', 'exportForHypervisor'

import re
import time
from rootobjectaction_lib import rootobjectaction_find, events
import uuid

def searchLocation(q, guid, request):
    mds = []
    for dcguid in rootobjectaction_find.datacenter_find(guid):
        for floor in rootobjectaction_find.floor_find(datacenterguid=dcguid):
            for rack in rootobjectaction_find.rack_find(floor=floor):
                mds += searchRack(q, rack, request)
    return mds

def searchDatacenter(q, guid, request):
    mds = []
    for floor in rootobjectaction_find.floor_find(datacenterguid=guid):
        for rack in rootobjectaction_find.rack_find(floor=floor):
            mds += searchRack(q, rack, request)
            
    return mds

def searchFloor(q, guid, request):
    mds = []
    for rack in rootobjectaction_find.rack_find(floor=guid):
        mds += searchRack(q, rack, request)
    return mds

def searchRoom(q, guid, request):
    mds = []
    for rack in rootobjectaction_find.rack_find(roomguid=guid):
        mds += searchRack(q, rack, request)
    return mds


def searchPod(q, guid, request):
    pod = q.drp.pod.get(guid)
    mds = []
    for rack in pod.racks:
        mds += searchRack(q, rack, request)
    
    for row in rootobjectaction_find.row_find(pod=guid):
        mds += searchRow(q, row)
    
    return mds

def searchRow(q, guid, request):
    row = q.drp.row.get(guid)
    mds = []
    for rack in row.racks:
        mds += searchRack(q, rack, request)
        
    return mds

def searchRack(q, guid, request):
    return rootobjectaction_find.meteringdevice_find(rackguid=guid)

def searchMeteringDevice(q, guid, request):
    return [guid]

def searchLogicalView(q, guid, request):
    results = q.actions.rootobject.logicalview.getViewResult(guid, request=request)['result']['info']
    meteringdevices = list()
    
    for result in results:
        type = result['type']
        objguid = result['guid']
        
        if type in SEARCH_OBJ:
            searchmethod = SEARCH_OBJ[type]
            meteringdevices += searchmethod(q, objguid, request)
    
    return meteringdevices
    

SEARCH_OBJ = {'location': searchLocation,
              'datacenter': searchDatacenter,
              'floor': searchFloor,
              'room': searchRoom,
              'pod': searchPod,
              'row': searchRow,
              'rack': searchRack,
              'meteringdevice': searchMeteringDevice,
              'logicalview': searchLogicalView} 


XML_PORT = """
<port status='%(status)s' tags_labels=''>
    <Current Actual='%(current)s' Min='%(mincurrent)s' Max='%(maxcurrent)s'/>
    <Power Actual='%(power)s' Min='%(minpower)s' Max='%(maxpower)s'/>
    <ApperentPower Actual='%(apparentpower)s' Min='%(minapparentpower)s' Max='%(maxapparentpower)s'/>
    <PowerFactor Actual='%(powerfactor)s' Min='%(minpowerfactor)s' Max='%(maxpowerfactor)s'/>
    <ActiveEnergy Actual='%(activeenergy)s'/>
    <ApparentEnergy Actual='%(apparentenergy)s'/>
</port>
"""

XML_SENSOR = """
<sensor sensortype='%(type)s' status='' tags_labels=''>
    <sensorvalue actual='%(value)s' max='%(max)s' min='%(min)s' />
</sensor>
"""

XML_DEVICE = """
<device firmwareversion="%(fwver)s" hardwareversion="%(hwver)s" ipaddress='%(ipaddress)s' tags_labels="%(tags)s" type="%(type)s">
    <ports>
        %(ports)s
    </ports>
    <sensors>
        %(sensors)s
    </sensors>
</device>
"""

XML_EXPORT = """<?xml version="1.0" encoding="ISO8859-1"?>
<export version="1.0" timestamp="%(timestamp)s" xsi:noNamespaceSchemaLocation="racktivitye_export.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <devices>
        %(devices)s
    </devices>
</export>
"""
def getPortsAndSensors(q, md):
    ports = []
    sensors = []
    for pp in md.poweroutputs:
        ports.append({'sequence': pp.sequence,
                      'label': pp.label})
    for sn in md.sensors:
        sensors.append({'sequence': sn.sequence,
                        'type': sn.type,
                        'label': sn.label})
    for mdguid in rootobjectaction_find.meteringdevice_find(parentmeteringdeviceguid=md.guid):
        submd = q.drp.meteringdevice.get(mdguid)
        subports, subsensors = getPortsAndSensors(q, submd)
        ports += subports
        sensors += subsensors
        
    return ports, sensors

def main(q, i, params, tags):
    params['result'] = {'returncode': False}
    
    rootobjectguid = params['rootobjectguid']
    returnformat = params['returnformat']
    
    obj = None
    searchmethod = None
    for type, search in SEARCH_OBJ.iteritems():
        objtype = getattr(q.drp, type)
        try:
            obj = objtype.get(rootobjectguid)
            searchmethod = search
        except:
            continue
    
    if not obj:
        events.raiseError("No object found with guid '%s'" % rootobjectguid, typeid=events.GENERIC_OBJECT_NOT_FOUND)
    
    meteringdevices = searchmethod(q, obj.guid, params['request'])
    
    pattern = re.compile("^", re.MULTILINE)
    indent = lambda x, s=4: re.sub(pattern, " "* s, x)
    
    devicesxml = []
    for mdguid in meteringdevices:
        #get it's data.
        md = q.drp.meteringdevice.get(mdguid)
        if md.parentmeteringdeviceguid:
            continue
        portsxml = []
        sensorsxml = []
        
        data = q.actions.rootobject.meteringdevice.getCurrentDeviceData(mdguid, "all")['result']['value']
        ports, sensors = getPortsAndSensors(q, md)
        
        for port in ports:
            portidx = port['sequence'] - 1
            portdata = data['Ports'][portidx]
            portsxml.append(XML_PORT % {'status': portdata['StatePortCur'],
                                       'current': portdata['Current'],
                                       'mincurrent': portdata.get('MinCurrent', 0),
                                       'maxcurrent': portdata.get('MaxCurrent', 0),
                                       'power': portdata.get('Power', 0),
                                       'minpower': portdata.get('MinPower', 0),
                                       'maxpower': portdata.get('MaxPower', 0),
                                       'apparentpower': portdata.get('ApparentPower', 0),
                                       'minapparentpower': portdata.get('MinApparentPower', 0),
                                       'maxapparentpower': portdata.get('MaxApparentPower', 0),
                                       'powerfactor': portdata.get('PowerFactor', 0),
                                       'minpowerfactor': portdata.get('MinPowerFactor', 0),
                                       'maxpowerfactor': portdata.get('MaxPowerFactor', 0),
                                       'activeenergy': portdata.get('ActiveEnergy', 0),
                                       'apparentenergy': portdata.get('ApparentEnergy', 0),
                                       })
            
        if 'Sensors' in data:
            for sensor in sensors:
                sensoridx = sensor['sequence'] - 1
                sensordata = data['Sensors'][sensoridx]
                sensorsxml.append(XML_SENSOR % {'type': sensor['type'],
                                                'value': sensordata['Value'],
                                                'max': sensordata['MaxValue'],
                                                'min': sensordata['MinValue']})
                
        rackappguid = rootobjectaction_find.racktivity_application_find(meteringdeviceguid=md.guid)
        rackapp = q.drp.racktivity_application.get(rackappguid[0])
        ipaddress = q.drp.ipaddress.get(rackapp.networkservices[0].ipaddressguids[0])
        
        devicesxml.append(XML_DEVICE % {'fwver': data.get('FirmwareVersion', ""),
                                  'hwver': data.get('HardwareVersion', ""),
                                  'ipaddress': ipaddress.address,
                                  'tags': md.tags if md.tags else '',
                                  'type': md.meteringdevicetype,
                                  'ports': indent("\n".join(portsxml)),
                                  'sensors': indent("\n".join(sensorsxml))})
    
    exportxml = XML_EXPORT % {'timestamp': int(time.time()),
                              'devices': indent("\n".join(devicesxml))}
    
    if returnformat == "raw":
        params['result'] = {'returncode': True, 'export': exportxml}
    elif returnformat == "filename":
        applicationguids = rootobjectaction_find.racktivity_application_find(name='racktivity_agent')
        agentguid = None
        if applicationguids:
            agentguid = applicationguids[0]
        else:
            events.raiseError("No Agent installed on this environment", messageprivate='', typeid=events.GENERIC_NO_AGENT_INSTALLED)
        filename = "%s.xml" % str(uuid.uuid4())
        expath = q.system.fs.joinPaths(q.dirs.baseDir, "www", filename)
        res = q.actions.actor.fs.writeFile(agentguid, expath, exportxml)
        rempath = "http://%s/%s" % (q.config.getConfig("agent")['main']['hostname'], filename)
        params['result'] = {'returncode': res['result']['returncode'], 'export': rempath}
    else:
        events.raiseError("Invalid export format, expecting 'raw' of 'filename'")

def match(q, i, params, tags):
    return True
