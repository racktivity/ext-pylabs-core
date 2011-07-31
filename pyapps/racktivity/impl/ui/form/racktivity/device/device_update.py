__tags__ = "wizard", "device_update"
__author__ = "racktivity"

DEVICE_NAME = "deviceName"
DEVICE_DESCRIPTION = "deviceDescription"
DEVICE_RACKU = "rackU"
DEVICE_RACKY = "rackY"
DEVICE_RACKZ = "rackZ"


def main(q,i,params,tags):
    cloudApi = i.config.cloudApiConnection.find('main')
    
    device = cloudApi.device.getObject(params['extra']['rootobjectguid'])
    
    form = q.gui.form.createForm()

    tab = form.addTab("main", "Add Device")

    tab.addText(DEVICE_NAME, "Name", value=device.name, message="The device name to add", optional=False)

    tab.addInteger(DEVICE_RACKU, "Rack U", value=device.racku, message='Size of the device, measured in u e.g. 1u high', minValue=1)
    tab.addInteger(DEVICE_RACKY, "Rack Y", value=device.racky, message='Physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1', minValue=1)
    tab.addInteger(DEVICE_RACKZ, "Rack Z", value=device.rackz, message='physical position of the device in the rack (z coordinate, 0 = front, 1 = back)', minValue=0, maxValue=1)

    tab.addMultiline(DEVICE_DESCRIPTION, "Description", value=device.description, message="Device description")

    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        deviceName = tab.elements[DEVICE_NAME].value
        tags = tab.elements['tags'].value
        matches = cloudApi.device.find(name=deviceName)['result']['guidlist']
        if matches and matches[0] != device.guid:
            tab.elements[DEVICE_NAME].status = "error"
            tab.elements[DEVICE_NAME].message = "A device with the same name already exists, please provide a unique name"
        elif tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        else:
            valid = True

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

    cloudApi.device.updateModelProperties(device.guid,
                           name=tab.elements[DEVICE_NAME].value,
                           description=tab.elements[DEVICE_DESCRIPTION].value,
                           racku=int(tab.elements[DEVICE_RACKU].value),
                           racky=int(tab.elements[DEVICE_RACKY].value),
                           rackz=int(tab.elements[DEVICE_RACKZ].value),
                           tags=tagstring)
    
    q.gui.dialog.showMessageBox("Device '%s' is being updated" % tab.elements[DEVICE_NAME].value, "Add Device")
    
def match(q,i,params,tags):
    return True