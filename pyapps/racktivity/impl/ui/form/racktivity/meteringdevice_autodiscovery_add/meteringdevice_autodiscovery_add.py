__tags__ = "wizard", "meteringdevice_autodiscovery_add"
__author__ = "racktivity"

IP_REGEX = "^((\d{1,2}|[0-1]\d{2}|2([0-4]\d|5[0-5]))\.){3}(\d{1,2}|[0-1]\d{2}|2([0-4]\d|5[0-5]))$"
DEFAULT_PASSWORD = "private"
DEFAULT_PORT = 161

from pylabs.pmtypes import IPv4Range

def getOrCreateLan(q, cloudapi, network, netmask):
    lans = cloudapi.lan.find(network=network, netmask=netmask)['result']['guidlist']
    if lans:
        return lans[0]
    
    backplaneguid = cloudapi.backplane.find()['result']['guidlist'][0]
    languid = cloudapi.lan.create(backplaneguid=backplaneguid, name='%s-%s' % (network, netmask), lantype=str(q.enumerators.lantype.STATIC),
                                 network=network, netmask=netmask)['result']['languid']
    return languid


def modelScannedDevice(q, cloudapi, device, netmask, name, rackguid):
    """
    Racktivity device.
    """
    #now model the racktivity device.
    address = device['address']
    range = IPv4Range(netIp=address, netMask=netmask)
    
    languid = getOrCreateLan(q, cloudapi, str(range.netIp), str(range.netMask))
    
    ipaddressguid = cloudapi.ipaddress.create(name=address, address=address, netmask=netmask, languid=languid)['result']['ipaddressguid']
    
    if device['type'] == 'PM0816':
        #special handle for racktivity device
        #model master module.
        masterguid = cloudapi.meteringdevice.create(name=name,
                                       id='M1',
                                       meteringdevicetype=str(q.enumerators.meteringdevicetype.PM0816),
                                       template=False,
                                       rackguid=rackguid,
                                       accounts=[{'login': "admin",
                                                  'password': 1234}],
                                       attributes = {'deviceapiportnr': device['apiport']},
                                       nicinfo = [{'ipaddressguids':[ipaddressguid], 'status':str(q.enumerators.nicstatustype.ACTIVE),
                                                   'nictype':str(q.enumerators.nictype.ETHERNET_GB), 'order':0}])['result']['meteringdeviceguid']
        #model power module.
        cloudapi.meteringdevice.create(name="%s-P1" % name,
                                       id='P1',
                                       meteringdevicetype=str(q.enumerators.meteringdevicetype.PM0816),
                                       template=False,
                                       rackguid=rackguid,
                                       parentmeteringdeviceguid=masterguid,
                                       poweroutputinfo=device['ports'])
        #model temperature module.
        cloudapi.meteringdevice.create(name="%s-T1" % (name),
                                       id='T1',
                                       meteringdevicetype=str(q.enumerators.meteringdevicetype.PM0816),
                                       template=False,
                                       rackguid=rackguid,
                                       parentmeteringdeviceguid=masterguid,
                                       sensorinfo=device['sensors'])
    else:
        #create a single device with ports/sensors and with the correct type
        masterguid = cloudapi.meteringdevice.create(name=name,
                                   id='M1',
                                   meteringdevicetype=str(device['type']),
                                   template=False,
                                   rackguid=rackguid,
                                   accounts=[{'login': '',
                                              'password': device['password']}],
                                   attributes = {'deviceapiportnr': str(device['apiport'])},
                                   nicinfo = [{'ipaddressguids':[ipaddressguid], 'status':str(q.enumerators.nicstatustype.ACTIVE),
                                               'nictype':str(q.enumerators.nictype.ETHERNET_GB), 'order':0}],
                                   poweroutputinfo=device['ports'],
                                   sensorinfo=device['sensors'] if 'sensors' in device else [])['result']['meteringdeviceguid']

def main(q, i, p, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    identified = cloudapi.meteringdevice.find(meteringdeviceconfigstatus=str(q.enumerators.meteringdeviceconfigstatus.IDENTIFIED))['result']['guidlist']
    
    devices = dict()
    for guid in identified:
        device = cloudapi.meteringdevice.getObject(guid)
        if device.parentmeteringdeviceguid:
            #only process the master metering devices.
            continue
        devices[guid] = device
    
    
    form = q.gui.form.createForm()
    
    tab = form.addTab("devices", "Found Devices")
    tab.message("note1", """Please select a deivce and press next to configured this auto discovered device.
If the deivce you want to add is not listed, go to the Manual scan tab and manually enter the IP
address you want to discover""")
    
    tab.addChoice("device", "Found Devices", dict([(key, device.name) for key, device in devices.iteritems()]), selectedValue='')
    
    scanTab = form.addTab("scan", "Manual Scan")
    scanTab.addText("ipaddress", "IP Address", validator=IP_REGEX, message="The ip address to discover")
    scanTab.addText("netmask", "Netmasek", validator=IP_REGEX, message="The netmask of the network")
    scanTab.addText("port", "SNMP Port", value=DEFAULT_PORT, validator="^\d+$")
    scanTab.addText("password", "Community String", value=DEFAULT_PASSWORD)
    
    guid = None
    ipaddress = None
    
    scanned = None
    sc_password = None
    sc_netmask = None
    
    while True:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['devices']
        guid = tab.elements['device'].value
        
        scanTab = form.tabs['scan']
        ipaddress = scanTab.elements['ipaddress'].value
        
        if ipaddress:
            sc_port = int(scanTab.elements['port'].value)
            sc_password = scanTab.elements['password'].value
            sc_netmask = scanTab.elements['netmask'].value
            if not sc_netmask:
                q.gui.dialog.showMessageBox("No netmask is given", "No netmask provided", msgboxIcon="Error")
                continue
            if cloudapi.ipaddress.find(address=ipaddress)['result']['guidlist']:
                q.gui.dialog.showMessageBox("IP address '%s' already taken by the system" % ipaddress, "IP Address is used", msgboxIcon="Error")
                continue
            
            scanresult = cloudapi.meteringdevice.discoverIpAddress(ipaddress, port=sc_port, communitystring=sc_password)['result']
            if not scanresult['returncode']:
                q.gui.dialog.showMessageBox("No device found on ip '%s'" % ipaddress, "No device found", msgboxIcon="Error")
                continue
            scanned = scanresult['device']
            break
        elif guid:
            break
        else:
            q.gui.dialog.showMessageBox("No Energy Switch was selected", "Please Select a device", msgboxIcon="Error")
    
    devicename = ""
    if scanned:
        devicename = "%s-%s" % (scanned['product'], ipaddress)
    else:
        device = devices[guid]
        devicename = device.name
    
    form = q.gui.form.createForm()
    
    rackguid = params['extra']['rackguid']
    conftab = form.addTab("config", "Baisc Configuration")
    
    conftab.addText("name", "Name", value=devicename, optional=False)
    conftab.addInteger('positionx', 'Position x', message='X position of the Energy Switch in rack', value=0)
    conftab.addInteger('positiony', 'Position y', message='Y position of the Energy Switch in rack', value=0)
    conftab.addInteger('positionz', 'Position z', message='Z position of the Energy Switch in rack', value=0)
    conftab.addInteger('height', 'Height', message='Height of the energy switch in U.', value=1)
    conftab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    conftab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    
    form.loadForm(q.gui.dialog.askForm(form))
    
    conftab = form.tabs['config']
    
    labels = None
    labelsvalue = conftab.elements['labels'].value
    if labelsvalue:
        labels = set(labelsvalue.split(','))

    tags = dict()
    tagsvalue = conftab.elements['tags'].value
    if tagsvalue:
        for tag in tagsvalue.split(','):
            tagslist = tag.split(':')
            tags[tagslist[0]] = tagslist[1]
    tagstring = q.base.tags.getTagString(labels, tags)
    
    if scanned:
        #model device from the scanned data.
        modelScannedDevice(q, cloudapi, scanned, sc_netmask, conftab.elements['name'].value, rackguid)
    else:
        cloudapi.meteringdevice.updateModelProperties(guid,
                                                      meteringdeviceconfigstatus=str(q.enumerators.meteringdeviceconfigstatus.CONFIGURED),
                                                      rackguid=rackguid,
                                                      name=conftab.elements['name'].value,
                                                      positionx=conftab.elements['positionx'].value,
                                                      positiony=conftab.elements['positiony'].value,
                                                      positionz=conftab.elements['positionz'].value,
                                                      tags=tagstring)
        
        for childguid in cloudapi.meteringdevice.find(parentmeteringdeviceguid=guid)['result']['guidlist']:
            cloudapi.meteringdevice.updateModelProperties(childguid,
                                                          meteringdeviceconfigstatus=str(q.enumerators.meteringdeviceconfigstatus.CONFIGURED),
                                                          rackguid=rackguid)
        
    q.gui.dialog.showMessageBox("Energy Switch '%s' has been added" % conftab.elements['name'].value, "Add Energy Switch")
    
def main(q, i, p, params, tags):
    return True