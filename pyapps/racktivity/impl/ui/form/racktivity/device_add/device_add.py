__tags__ = "wizard", "device_add"
__author__ = "racktivity"

import collections
import re

DEVICE_NAME = "deviceName"
DEVICE_TYPE = "deviceType"
DEVICE_DESCRIPTION = "deviceDescription"
DEVICE_TEMPLATE = "template"
DEVICE_RACKU = "rackU"
DEVICE_RACKY = "rackY"
DEVICE_RACKZ = "rackZ"

DEVICE_PORTS_TAB = "ports"
PORTS_NUMBER = "portsNumber"

TEMPLATE_NOTEMPLATE = "notemplate"

def getTemplatesOfType(cloudApi, type):
    templatesguids = cloudApi.device.find(devicetype=str(type),
                        template=True)['result']['guidlist']
    
    results = {TEMPLATE_NOTEMPLATE: 'No Template'}
    for templateguid in templatesguids:
        template = cloudApi.device.getObject(templateguid)
        results[templateguid] = template.name

    return results

def callback_numberofports_change(q,i,params,tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    portstab = form.tabs[DEVICE_PORTS_TAB]
    buildPortsTab(q, portstab, portstab.elements[PORTS_NUMBER].value)
    return form

def buildPortsTab(q, tab, numberOfPorts=1):
    #remove old elements
    cache = dict()

    names = [e.name for e in tab.elements]
    
    for name in names:
        if name.startswith("powerport-"):
            cache[name] = tab.elements[name].value
        tab.removeElement(name)
            
    tab.addInteger(PORTS_NUMBER, "Number of ports", minValue=1, value=numberOfPorts,
                   trigger="change", callback="numberofports_change")
    
    for i in xrange(numberOfPorts):
        name = "powerport-%s-sequence" % i
        tab.addInteger(name, "Port %d Sequence" % (i+1), minValue=0)
        if name in cache:
            tab.elements[name].value = cache[name]
        name = "powerport-%s-name" % i
        tab.addText(name, "Port %d Label" % (i+1), optional=False)
        if name in cache:
            tab.elements[name].value = cache[name]

def callback_type_change(q,i,params,tags):
    cloudApi = p.api.action.racktivity

    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    tab = form.tabs['main']
    type = tab.elements[DEVICE_TYPE].value

    templates = getTemplatesOfType(cloudApi, q.enumerators.devicetype.getByName(type))
    tab.elements[DEVICE_TEMPLATE].values = templates
    tab.elements[DEVICE_TEMPLATE].value = TEMPLATE_NOTEMPLATE
    return form

def callback_template_change(q, i, params, tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])

    tab = form.tabs['main']
    templateguid = tab.elements[DEVICE_TEMPLATE].value
    if templateguid != TEMPLATE_NOTEMPLATE:
        form.removeTab(DEVICE_PORTS_TAB)
    else:
        portstab =  form.tabs[DEVICE_PORTS_TAB] if DEVICE_PORTS_TAB in form.tabs else form.addTab(DEVICE_PORTS_TAB, "Power Ports")
        buildPortsTab(q, portstab, 1)

    return form

def checkDeviceNameUnique(cloudApi, name):
    return not bool(cloudApi.device.find(name=name)['result']['guidlist'])

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity
    form = q.gui.form.createForm()

    tab = form.addTab("main", "Add Device")

    tab.addText(DEVICE_NAME, "Name", message="The device name to add", optional=False)
    types = dict([(k, k.capitalize()) for k in q.enumerators.devicetype._pm_enumeration_items.keys()])
    tab.addChoice(DEVICE_TYPE, "Type", types,
                  message="The device type", trigger='change', callback='type_change', optional=False)

    tab.elements[DEVICE_TYPE].value = str(q.enumerators.devicetype.COMPUTER)

    tab.addChoice(DEVICE_TEMPLATE, "Template", message="Create device from template",
                  trigger = "change", callback = "template_change",
                  values = getTemplatesOfType(cloudApi, q.enumerators.devicetype.COMPUTER), selectedValue=TEMPLATE_NOTEMPLATE, optional=False)

    tab.addInteger(DEVICE_RACKU, "Rack U", message='Size of the device, measured in u e.g. 1u high', minValue=1)
    tab.addInteger(DEVICE_RACKY, "Rack Y", message='Physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1', minValue=1)
    tab.addInteger(DEVICE_RACKZ, "Rack Z", message='physical position of the device in the rack (z coordinate, 0 = front, 1 = back)', minValue=0, maxValue=1)

    tab.addMultiline(DEVICE_DESCRIPTION, "Description", message="Device description")

    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')

    tab = form.addTab(DEVICE_PORTS_TAB, "Power Ports")
    buildPortsTab(q, tab)
    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        tags = tab.elements['tags'].value
        deviceName = tab.elements[DEVICE_NAME].value
        if not checkDeviceNameUnique(cloudApi, deviceName):
            tab.elements[DEVICE_NAME].status = "error"
            tab.elements[DEVICE_NAME].message = "A device with the same name already exists, please provide a unique name"
        elif tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        else:
            valid = True
        
        if not tab.elements[DEVICE_TEMPLATE].value:
            #user has defined ports manually.
            portstab = form.tabs[DEVICE_PORTS_TAB]
            portsname = list()
            for pe in portstab.elements:
                m = re.match("^powerport-(\d+)-name$", pe.name)
                if m:
                    if pe.value not in portsname:
                        portsname.append(pe.value)
                    else:
                        pe.status = "error"
                        pe.message = "Port label must be unique"
                        valid = False
                        break

    #create the device.
    tab = form.tabs['main']
    ports = collections.defaultdict(dict)
    if tab.elements[DEVICE_TEMPLATE].value != TEMPLATE_NOTEMPLATE:
        template = cloudApi.device.getObject(tab.elements[DEVICE_TEMPLATE].value)
        i = 0
        for i, powerport in enumerate(template.powerports):
            ports[i] = {'name': powerport.name, 'status': str(q.enumerators.powerportstatustype.NOTCONNECTED), 'sequence': powerport.sequence}
    else:
        portstab = form.tabs[DEVICE_PORTS_TAB] 
        for pe in portstab.elements:
            m = re.match("^powerport-(\d+)-(.+)$", pe.name)
            if m:
                index = int(m.group(1))
                attr = m.group(2)
                ports[index][attr] = str(pe.value)
        for port in ports.itervalues():
            port['status'] = str(q.enumerators.powerportstatustype.NOTCONNECTED)

    labels = None
    labelsvalue = tab.elements['labels'].value
    if labelsvalue:
        labels = set(labelsvalue.split(','))

    tags = dict()
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in tagsvalue.split(','):
            tagslist = tag.split(':')
            tags[tagslist[0]] = tagslist[1]
    tagstring = q.base.tags.getTagString(labels, tags)

    cloudApi.device.create(name=tab.elements[DEVICE_NAME].value,
                           #datacenterguid = params['extra']['datacenterguid'],
                           rackguid = params['extra']['rackguid'],
                           devicetype=tab.elements[DEVICE_TYPE].value,
                           description=tab.elements[DEVICE_DESCRIPTION].value,
                           racku=int(tab.elements[DEVICE_RACKU].value),
                           racky=int(tab.elements[DEVICE_RACKY].value),
                           rackz=int(tab.elements[DEVICE_RACKZ].value),
                           powerports = ports.values(),
                           tags=tagstring)
    
    q.gui.dialog.showMessageBox("Device '%s' is being added" % tab.elements[DEVICE_NAME].value, "Add Device")
    
def match(q, i, p, params, tags):
    return True
