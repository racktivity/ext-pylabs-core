__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_add'

import re
import collections
from pylabs.pmtypes import IPv4Range, IPv4Address

REGEX_IP4ADDRESS_VALIDATOR = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

def getNetworkIP(ipaddress, netmask):
    ip = ipaddress.split(".")
    netm = netmask.split(".")
    network = str(int(ip[0]) & int(netm[0]))+"."+str(int(ip[1]) & int(netm[1]))+"."+str(int(ip[2]) & int(netm[2]))+"."+str(int(ip[3]) & int(netm[3]))
    return network

def checkGatewayInNetwork(tab):
    valid = True
    netmask = tab.elements['netmask'].value
    gateway = tab.elements['gateway'].value
    ipaddress = tab.elements['ipaddress'].value    
    if not IPv4Address(gateway) in IPv4Range(netIp=getNetworkIP(ipaddress, netmask), netMask=netmask):
        valid = False
        tab.elements['gateway'].status = 'error'
        tab.elements['gateway'].message = 'Gateway is not in the same network, provide a correct one'
    else:
        tab.elements['gateway'].status = ''
        tab.elements['gateway'].message = ''
    return valid

def createLanAndIpaddress(q, cloudapi, tab):
    netmask = tab.elements['netmask'].value
    dns = list()
    dns.append(tab.elements['dns'].value)
    ipaddress = tab.elements['ipaddress'].value
    gateway = tab.elements['gateway'].value
    languids = cloudapi.lan.find(network=getNetworkIP(ipaddress, netmask), netmask=netmask)['result']['guidlist']
    if languids:
        #Add the ipaddress to the existing lan
        languid = languids[0]
    else:
        #Create new lan
        backplaneguid = cloudapi.backplane.find()['result']['guidlist'][0]
        languid = cloudapi.lan.create(backplaneguid=backplaneguid, name='%s-%s' % (getNetworkIP(ipaddress, netmask), netmask),
                                      lantype=str(q.enumerators.lantype.STATIC),
                                      network=getNetworkIP(ipaddress, netmask), netmask=netmask, gateway=gateway, dns=dns)['result']['languid']
    ipaddressguid = cloudapi.ipaddress.create(name=ipaddress, address=ipaddress, netmask=netmask, languid=languid)['result']['ipaddressguid']
    return ipaddressguid

def checkLanExists(q, cloudapi, tab):
    valid = True
    netmask = tab.elements['netmask'].value
    ipaddress = tab.elements['ipaddress'].value
    languids = cloudapi.lan.find(network=getNetworkIP(ipaddress, netmask), netmask=netmask)['result']['guidlist']
    if languids:
        #Add the ipaddress to the existing lan
        languid = languids[0]
        if cloudapi.ipaddress.find(address=ipaddress, netmask=netmask, languid=languid)['result']['guidlist']:
            valid = False
            tab.elements['ipaddress'].status = 'error'
            tab.elements['ipaddress'].message = 'Ipaddress with value "%s" already exists, provide another one' % ipaddress
        else:
            tab.elements['ipaddress'].status = ''
            tab.elements['ipaddress'].message = ''
    return valid

def callback_numberofports_change(q, i, params, tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    portstab = form.tabs['ports']
    buildPortsTab(q, portstab, portstab.elements['num_port'].value)
    return form

def callback_numberofpowerinputs_change(q, i, params, tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    powerinputstab = form.tabs['powerinputs']
    buildPowerInputsTab(q, powerinputstab, powerinputstab.elements['num_powerinput'].value)
    return form

def callback_numberofpoweroutputs_change(q, i, params, tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    poweroutputstab = form.tabs['poweroutputs']
    buildPowerOutputsTab(q, poweroutputstab, poweroutputstab.elements['num_poweroutput'].value)
    return form

def callback_numberofsensors_change(q, i, params, tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    sensorstab = form.tabs['sensors']
    buildSensorsTab(q, sensorstab, sensorstab.elements['num_sensor'].value)
    return form

def callback_chooseFeed(q, i, params, tags):
    cloudapi = p.api.action.racktivity
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    tab = form.tabs['main']
    datacenterguid = params['SESSIONSTATE']['datacenterguid']
    if tab.elements['feed'].value:
        feedguids = cloudapi.feed.find(datacenterguid=datacenterguid)['result']['guidlist']
        if feedguids:
            feeds = [cloudapi.feed.getObject(feedguid) for feedguid in feedguids]
            feedsdict = dict([(feed.guid, feed.name) for feed in feeds])
            tab.addChoice('feedguid', 'Select Feed', feedsdict, optional=False)
        else:
            tab.elements['feed'].message = 'No Feeds created on this datacenter'
            tab.elements.status = 'error'
    return form
    
def buildPortsTab(q, tab, numberOfPorts=0):
    cache = dict()
    porttypes = dict([(k, k.capitalize()) for k in q.enumerators.porttype._pm_enumeration_items.keys()])
    names = [e.name for e in tab.elements]

    for name in names:
        if name.startswith("port-"):
            cache[name] = tab.elements[name].value
        tab.removeElement(name)

    tab.addInteger('num_port', "Number of ports", minValue=0, value=numberOfPorts,
                   trigger="change", callback="numberofports_change")

    for i in xrange(numberOfPorts):
        name = "port-%s-sequence" % i
        tab.addInteger(name, "Port %d Sequence" % (i+1), minValue=i+1)
        if name in cache:
            tab.elements[name].value = cache[name]
        name = "port-%s-label" % i
        tab.addText(name, "Port %d Label" % (i+1))
        if name in cache:
            tab.elements[name].value = cache[name]

        name = "port-%s-porttype" % i
        tab.addChoice(name, "Port %d type" % (i+1), values=porttypes)
        if name in cache:
            tab.elements[name].value = cache[name]

def buildPowerInputsTab(q, tab, numberOfPorts=0):
    cache = dict()
    names = [e.name for e in tab.elements]

    for name in names:
        if name.startswith("powerinput-"):
            cache[name] = tab.elements[name].value
        tab.removeElement(name)

    tab.addInteger('num_powerinput', "Number of power input ports", minValue=0, value=numberOfPorts,
                   trigger="change", callback="numberofpowerinputs_change")

    for i in xrange(numberOfPorts):
        name = "powerinput-%s-sequence" % i
        tab.addInteger(name, "Power input %d Sequence" % (i+1), minValue=i+1)
        if name in cache:
            tab.elements[name].value = cache[name]
        name = "powerinput-%s-label" % i
        tab.addText(name, "Power input port %d Label" % (i+1))
        if name in cache:
            tab.elements[name].value = cache[name]

def buildPowerOutputsTab(q, tab, numberOfPorts=0):
    cache = dict()
    names = [e.name for e in tab.elements]

    for name in names:
        if name.startswith("poweroutput-"):
            cache[name] = tab.elements[name].value
        tab.removeElement(name)

    tab.addInteger('num_poweroutput', "Number of power output ports", minValue=0, value=numberOfPorts,
                   trigger="change", callback="numberofpoweroutputs_change")

    for i in xrange(numberOfPorts):
        name = "poweroutput-%s-sequence" % i
        tab.addInteger(name, "Power output %d Sequence" % (i+1), minValue=i+1)
        if name in cache:
            tab.elements[name].value = cache[name]
        name = "poweroutput-%s-label" % i
        tab.addText(name, "Power output port %d Label" % (i+1))
        if name in cache:
            tab.elements[name].value = cache[name]

def buildSensorsTab(q, tab, numberOfSensors=0):
    cache = dict()
    sensortypes = dict([(k, k.capitalize().replace('sensor', ' sensor')) for k in q.enumerators.sensortype._pm_enumeration_items.keys()])
    names = [e.name for e in tab.elements]

    for name in names:
        if name.startswith("sensor-"):
            cache[name] = tab.elements[name].value
        tab.removeElement(name)

    tab.addInteger('num_sensor', "Number of sensors", minValue=0, value=numberOfSensors,
                   trigger="change", callback="numberofsensors_change")

    for i in xrange(numberOfSensors):
        name = "sensor-%s-sequence" % i
        tab.addInteger(name, "Sensor %d Sequence" % (i+1), minValue=i+1)
        if name in cache:
            tab.elements[name].value = cache[name]

        name = "sensor-%s-label" % i
        tab.addText(name, "Sensor %d Label" % (i+1))
        if name in cache:
            tab.elements[name].value = cache[name]

        name = "sensor-%s-sensortype" % i
        tab.addChoice(name, "Sensor %d Type" % (i+1), values=sensortypes)
        if name in cache:
            tab.elements[name].value = cache[name]

def validateLabel(tab, fieldname):
    valid = True
    fields = list()
    for element in tab.elements:
        match = re.match("^%s-(\d+)-label$" % fieldname, element.name)
        if match:
            if element.value not in fields:
                fields.append(element.value)
            else:
                valid = False
                element.status = "error"
                element.message = "%s Label must be unique" % fieldname
                break
    return valid

def getFields(cloudapi, form, fieldname, elementname, keys, tabname):
    tab = form.tabs['main']
    fields = collections.defaultdict(dict)
    tab = form.tabs[tabname] 
    for element in tab.elements:
        match = re.match("^%s-(?P<index>\d+)-(?P<attr>.+)$" % elementname, element.name)
        if match:
            index = int(match.group("index"))
            attr = match.group("attr")
            fields[index][attr] = element.value
    return fields

def connectFeed(q, cloudapi, feedguid, powerinputs, mdguid):
    for powerinput in powerinputs.values():
        cablelabel = 'cable_%s_%s' % (mdguid, powerinput['label'])
        returnedvalue = cloudapi.cable.create(cablelabel, str(q.enumerators.cabletype.POWERCABLE))
        cableguid = returnedvalue['result']['cableguid']
        connectorname = 'connector_%s_%s' % (mdguid, powerinput['label'])
        cloudapi.feed.addConnector(feedguid, connectorname, 0, str(q.enumerators.feedConnectorStatusType.NOTCONNECTED))
        cloudapi.feed.connectConnector(feedguid, connectorname, cableguid)
        powerinput['cableguid'] = cableguid
        
def getTagString(q, tab):
    labels = None
    labelsvalue = tab.elements['labels'].value
    trim = lambda s: s.strip()
    if labelsvalue:
        labels = set(map(trim, labelsvalue.split(',')))
        
    tags = dict()
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in map(trim, tagsvalue.split(',')):
            tagslist = tag.split(':')
            tags[tagslist[0].strip()] = tagslist[1].strip()
    return q.base.tags.getTagString(labels, tags)

def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    module = False
    nics = list()
    accounts = list()
    attributes = dict()
    rackguid = params['extra']['rackguid']
    rack = cloudapi.rack.getObject(rackguid)
    datacenterguid = None
    if rack.roomguid:
        room = cloudapi.room.getObject(rack.roomguid)
        datacenterguid = room.datacenterguid
    elif rack.floor:
        floor = cloudapi.floor.getObject(rack.floor)
        datacenterguid = floor.datacenterguid
        
    if not datacenterguid:
        raise RuntimeError("Can't find datacenter")
    
    params['SESSIONSTATE']['datacenterguid'] = datacenterguid
    parentmeteringdeviceguid = None
    if 'parentmeteringdeviceguid' in params['extra']:
        parentmeteringdeviceguid = params['extra']['parentmeteringdeviceguid']
        module = True

    form = q.gui.form.createForm()
    tab = form.addTab("main", "General")
    tab.addText('name', "Name", message="Enter Energy Switch name", optional=False)
    if module:
        tab.addText('id', "Energy Switch Id", message='id of the device (e.g T1, P1, ...)', optional=False)
    types = dict([(k, k.capitalize()) for k in q.enumerators.meteringdevicetype._pm_enumeration_items.keys()])
    tab.addDropDown('type', "Type", types, message="The device type", optional=False)
    tab.addInteger('positionx', 'Units in Rack', message='Units in the rack occupied by the Energy Switch', value=0, minValue=0)
    tab.addInteger('positiony', 'Vertical Position', message='Vertical position of the Energy Switch in rack', value=0, minValue=0)
    tab.addInteger('positionz', 'Horizontal Position', message='Horizontal position of the Energy Switch in rack', value=0, minValue=0)
    tab.addInteger('height', 'Height', message='Height of the energy switch in U.', value=1, minValue=0)
    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    if module:
        tab.addYesNo('feed', 'Connect to Feed?', trigger='change', callback='chooseFeed')

    if not module:
        #Network Configuration
        networktab = form.addTab('network', 'Networking')
        networktab.addText('ipaddress', 'Ipaddress', validator=REGEX_IP4ADDRESS_VALIDATOR, optional=False)
        networktab.addText('netmask', 'Netmask', validator=REGEX_IP4ADDRESS_VALIDATOR, optional=False)
        networktab.addText('gateway', 'Gateway', validator=REGEX_IP4ADDRESS_VALIDATOR, optional=False)
        networktab.addText('dns', 'DNS', validator=REGEX_IP4ADDRESS_VALIDATOR, optional=False)
        networktab.addInteger('deviceapiportnr', 'Device Port Number', optional=True, value=80)

        #Accounts tab
        accounttab = form.addTab('account', 'Account')
        #Currently we create one account on the meteringdevice
        accounttab.addText('login', 'Login', optional=False)
        accounttab.addPassword('password', 'Password', optional=False)
        accounttab.addPassword('password-validation', 'Confirm password', optional=False)

    powerinputtab = form.addTab('powerinputs', 'Power Inputs')
    poweroutputtab = form.addTab('poweroutputs', 'Power Outputs')
    portstab = form.addTab('ports', 'Ports')
    sensorstab = form.addTab('sensors', 'Sensors')

    buildPortsTab(q, portstab)
    buildPowerInputsTab(q, powerinputtab)
    buildPowerOutputsTab(q, poweroutputtab)
    buildSensorsTab(q, sensorstab)

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        meteringdeviceName = tab.elements['name'].value
        tags = tab.elements['tags'].value
        valid = True
        if cloudapi.meteringdevice.find(name=meteringdeviceName)['result']['guidlist']:
            tab.elements['name'].status = "error"
            tab.elements['name'].message = "An Energy Switch with the same name already exists, please provide a unique name"
            valid = False
        elif 'account' in form.tabs:
            accounttab = form.tabs['account']
            if accounttab.elements['password'].value != accounttab.elements['password-validation'].value:
                accounttab.elements['password'].status = 'error'
                accounttab.elements['password'].message = 'Passwords do not match'
                valid = False
        elif tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
            valid = False
        valid &= validateLabel(form.tabs['ports'], 'port') and validateLabel(form.tabs['poweroutputs'], 'poweroutput') \
        and validateLabel(form.tabs['powerinputs'], 'powerinput')
        if 'network' in form.tabs:
            networktab = form.tabs['network']
            valid &= checkGatewayInNetwork(networktab) and checkLanExists(q, cloudapi, networktab)

    if 'id' in tab.elements:
        id = tab.elements['id'].value
    else:
        id = 'M1'

    if 'network' in form.tabs:
        networktab = form.tabs['network']
        ipaddressguid = createLanAndIpaddress(q, cloudapi, networktab)
        #Add a nic to the meteringdevice with the created ipaddress
        nics = [{'ipaddressguids':[ipaddressguid], 'status':str(q.enumerators.nicstatustype.ACTIVE),
         'nictype':str(q.enumerators.nictype.ETHERNET_GB), 'order':0}]
        attributes = {'deviceapiportnr': str(networktab.elements['deviceapiportnr'].value)}

    if 'account' in form.tabs:
        accounttab = form.tabs['account']
        accounts = [{'login': accounttab.elements['login'].value, 'password': accounttab.elements['password'].value}]

    ports = getFields(cloudapi, form, 'ports', 'port', ['label', 'sequence', 'porttype'], 'ports')
    poweroutputs = getFields(cloudapi, form, 'poweroutputs', 'poweroutput', ['label', 'sequence'], 'poweroutputs')
    powerinputs = getFields(cloudapi, form, 'powerinputs', 'powerinput', ['label', 'sequence'], 'powerinputs')
    sensors = getFields(cloudapi, form, 'sensors', 'sensor', ['label', 'sequence', 'sensortype'], 'sensors')

    meteringdevicetype = str(q.enumerators.meteringdevicetype.getByName(tab.elements['type'].value))

    clouduserguid = params['extra']['clouduserguid'] if 'clouduserguid' in params['extra'] else None

    feedguid = None
    if 'feedguid' in tab.elements and tab.elements['feedguid'].value:
        feedguid = tab.elements['feedguid'].value
    if feedguid and powerinputs.keys():
        connectFeed(q, cloudapi, feedguid, powerinputs, parentmeteringdeviceguid)
    elif feedguid and not powerinputs.keys():
        tab.elements['feed'].message = 'No power inputs are added to the Energy Switch, cannot add/connect feeds'
        tab.elements['feed'].status = 'error'

    tagstring = getTagString(q, tab)

    cloudapi.meteringdevice.create(name=tab.elements['name'].value,
                                   id=id,
                                   meteringdevicetype=meteringdevicetype,
                                   template=False,
                                   rackguid=rackguid,
                                   clouduserguid=clouduserguid,
                                   parentmeteringdeviceguid=parentmeteringdeviceguid,
                                   height=tab.elements['height'].value,
                                   positionx=tab.elements['positionx'].value,
                                   positiony=tab.elements['positiony'].value,
                                   positionz=tab.elements['positionz'].value,
                                   portsinfo=ports.values(),
                                   poweroutputinfo=poweroutputs.values(),
                                   powerinputinfo=powerinputs.values(),
                                   sensorinfo=sensors.values(),
                                   accounts=accounts,
                                   nicinfo=nics,
                                   attributes=attributes,
                                   tags=tagstring)

    q.gui.dialog.showMessageBox("Energy Switch '%s' is being added" % tab.elements['name'].value, "Add Energy Switch")

def match(q, i, p, params, tags):
    return True
